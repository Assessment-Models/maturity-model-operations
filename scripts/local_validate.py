#!/usr/bin/env python3
"""Level 1 local validation for Operations Maturity Model 2.1.0.

Validates canonical scale identity, legacy crosswalk, assessment-status semantics,
canonical score-band resolution, marginal-band EAV, worked examples and manifest
handshake. Exits non-zero and lists every detected failure.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []


def load(rel: str):
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"missing file: {rel}")
        return {}
    try:
        return yaml.safe_load(path.read_text()) or {}
    except yaml.YAMLError as exc:
        errors.append(f"invalid YAML in {rel}: {exc}")
        return {}


manifest = load("model.yaml")
scale = load("maturity/scale.yaml")
register = load("maturity/model/operations.yaml")
criteria_register = load("maturity/model/operations-v2-draft.yaml")
evaluation = load("maturity/evaluation.yaml")
questionnaire = load("maturity/assessment-questionnaire.yaml")
evidence_schema = load("maturity/evidence/schema.yaml")
migration = load("migrations/scale-v1-to-v2-map.yaml")
example = load("examples/operations-2026.yaml")
campaign = load("campaigns/baseline-vs-target-2026.yaml")

# Manifest and handshake.
for key in ("id", "type", "name", "version", "conformance"):
    if key not in manifest:
        errors.append(f"model.yaml: missing required field {key}")
if manifest.get("type") not in ("maturity-model", "assessment-model", "assessment-tool"):
    errors.append(f"model.yaml: invalid type {manifest.get('type')!r}")
if manifest.get("version") != "2.1.0":
    errors.append(f"model.yaml: expected version 2.1.0, found {manifest.get('version')!r}")
conf = manifest.get("conformance") or {}
if not (conf.get("contract") or {}).get("id") or not conf.get("version"):
    errors.append("model.yaml: incomplete contract handshake")
source = conf.get("source") or {}
if not source.get("organization") or not source.get("repository"):
    errors.append("model.yaml: conformance source organization/repository required")

# Canonical scale: L-0 sentinel plus five assessed capability levels.
EXPECTED = [
    ("L-0", 0, "Not Assessed"),
    ("L-1", 1, "Emergent"),
    ("L-2", 2, "Structured"),
    ("L-3", 3, "Systematic"),
    ("L-4", 4, "Adaptive"),
    ("L-5", 5, "Self-Optimising"),
]
levels = scale.get("levels") or []
actual = [(x.get("id"), x.get("ordinal"), x.get("name")) for x in levels]
if actual != EXPECTED:
    errors.append(f"scale: expected canonical levels {EXPECTED!r}, found {actual!r}")
if scale.get("id") != "dea:scale-operations-v2":
    errors.append("scale: id must be dea:scale-operations-v2")
if scale.get("version") != "2.0.0":
    errors.append("scale: version must be 2.0.0")
if scale.get("ordering") != "ascending":
    errors.append("scale: ordering must be ascending")
if (scale.get("progression") or {}).get("effort_multiplier") != {
    "L-1": 1.0, "L-2": 1.5, "L-3": 2.5, "L-4": 4.0, "L-5": 6.0
}:
    errors.append("scale: effort multipliers do not match canonical v2 values")
sentinel = next((x for x in levels if x.get("id") == "L-0"), {})
if "not a capability level" not in str(sentinel.get("definition", "")).lower():
    errors.append("scale: L-0 must be explicitly defined as a non-capability sentinel")

# Model bindings.
for label, obj in (("model register", register), ("criteria register", criteria_register)):
    if obj.get("repo_id") != manifest.get("id"):
        errors.append(f"{label}: repo_id does not match model manifest")
    if obj.get("scale_levels") != ["L-1", "L-2", "L-3", "L-4", "L-5"]:
        errors.append(f"{label}: scale_levels must reference L-1..L-5 only")
    if obj.get("unassessed_level") != "L-0":
        errors.append(f"{label}: unassessed_level must be L-0")
    if (obj.get("scale_reference") or {}).get("id") != "dea:scale-operations-v2":
        errors.append(f"{label}: missing canonical Operations scale reference")

# Assessment record semantics.
record_schema = evidence_schema.get("assessment_record") or {}
score_entry = record_schema.get("criterion_score") or {}
if score_entry.get("required") != ["level_id", "assessment_status", "score", "evidence_confidence"]:
    errors.append("evidence schema: criterion_score required fields are incomplete")
score_rules = score_entry.get("rules") or []
if not any("L-0 requires" in str(rule) and "unverified" in str(rule) for rule in score_rules):
    errors.append("evidence schema: L-0 must require not-assessed, score 0 and unverified confidence")
if not any("legacy L0" in str(rule) and "L-1" in str(rule) for rule in score_rules):
    errors.append("evidence schema: legacy L0 must be distinguished from canonical L-0")

# Questionnaire response scale.
response_scale = questionnaire.get("response_scale") or {}
if response_scale.get("assessed_levels") != ["L-1", "L-2", "L-3", "L-4", "L-5"]:
    errors.append("questionnaire: assessed_levels must be L-1..L-5")
if response_scale.get("unassessed_level") != "L-0":
    errors.append("questionnaire: unassessed_level must be L-0")
if response_scale.get("score_mapping") != {
    "L-1": 0, "L-2": 25, "L-3": 50, "L-4": 75, "L-5": 100
}:
    errors.append("questionnaire: score mapping is incorrect")

# Legacy compatibility map: L0 is Emergent, not the new L-0 sentinel.
legacy = ((migration.get("mapping") or {}).get("legacy_levels") or {})
if legacy != {"L0": "L-1", "L1": "L-2", "L2": "L-3", "L3": "L-4", "L4": "L-5"}:
    errors.append(f"migration: unexpected legacy level mapping {legacy!r}")
unassessed = ((migration.get("mapping") or {}).get("new_unassessed_state") or {})
if unassessed.get("id") != "L-0" or unassessed.get("legacy_equivalent") is not None:
    errors.append("migration: L-0 must have no legacy equivalent")
if migration.get("status") != "stable":
    errors.append("migration: scale crosswalk must be stable")

# Canonical bands use continuous intervals so fractional Operations Index values
# resolve without gaps. Each band contributes only the score points within it.
BANDS = [
    ("level-1-emergent", 0.0, 20.0, 1.0, "L-1"),
    ("level-2-structured", 20.0, 45.0, 1.5, "L-2"),
    ("level-3-systematic", 45.0, 70.0, 2.5, "L-3"),
    ("level-4-adaptive", 70.0, 88.0, 4.0, "L-4"),
    ("level-5-self-optimising", 88.0, 100.0, 6.0, "L-5"),
]


def resolve_band(score: float):
    if score < 0 or score > 100:
        return None
    for index, (band_id, lower, upper, multiplier, level_id) in enumerate(BANDS):
        if (score >= lower and score <= upper) if index == 0 else (score > lower and score <= upper):
            return band_id, level_id
    return None


def eav(score: float) -> float:
    if score < 0 or score > 100:
        raise ValueError("Operations Index must be within [0,100]")
    total = 0.0
    for index, (_, lower, upper, multiplier, _) in enumerate(BANDS):
        points = max(0.0, min(score, upper) - lower) if index else max(0.0, min(score, upper))
        total += points / multiplier
    return total


# Formula boundary checks and maximum.
boundary_expected = {
    0: 0.0,
    20: 20.0,
    45: 20 + 25 / 1.5,
    70: 20 + 25 / 1.5 + 25 / 2.5,
    88: 20 + 25 / 1.5 + 25 / 2.5 + 18 / 4.0,
    100: 20 + 25 / 1.5 + 25 / 2.5 + 18 / 4.0 + 12 / 6.0,
}
for score, expected in boundary_expected.items():
    if not math.isclose(eav(float(score)), expected, abs_tol=1e-9):
        errors.append(f"EAV boundary {score}: expected {expected}, found {eav(float(score))}")
if not math.isclose(eav(100.0), 53.1666666667, abs_tol=1e-9):
    errors.append("EAV: theoretical maximum is not 53.1666666667")

# Worked example.
score = example.get("aggregated_score")
if not isinstance(score, (int, float)) or not 0 <= score <= 100:
    errors.append("example: aggregated_score must be numeric and within [0,100]")
else:
    resolved = resolve_band(float(score))
    if not resolved:
        errors.append("example: Operations Index does not resolve to a canonical band")
    else:
        band_id, level_id = resolved
        if example.get("resolved_band") != band_id:
            errors.append(f"example: expected band {band_id}, found {example.get('resolved_band')!r}")
        if example.get("resolved_level") != level_id:
            errors.append(f"example: expected level {level_id}, found {example.get('resolved_level')!r}")
        expected_eav = round(eav(float(score)), 2)
        if not math.isclose(float(example.get("effort_adjusted_value", -1)), expected_eav, abs_tol=0.01):
            errors.append(f"example: expected marginal EAV {expected_eav}, found {example.get('effort_adjusted_value')!r}")

# Campaign examples and deltas.
for key in ("baseline", "target"):
    record = campaign.get(key) or {}
    index = record.get("operations_index")
    if not isinstance(index, (int, float)):
        errors.append(f"campaign {key}: operations_index must be numeric")
        continue
    band = resolve_band(float(index))
    if not band:
        errors.append(f"campaign {key}: no canonical band for score {index}")
        continue
    if record.get("resolved_band") != band[0] or record.get("resolved_level") != band[1]:
        errors.append(f"campaign {key}: maturity resolution does not match score {index}")
    expected = round(eav(float(index)), 2)
    if not math.isclose(float(record.get("effort_adjusted_value", -1)), expected, abs_tol=0.01):
        errors.append(f"campaign {key}: expected EAV {expected}, found {record.get('effort_adjusted_value')!r}")
deltas = campaign.get("deltas") or {}
expected_delta = round(
    eav(float((campaign.get("target") or {}).get("operations_index", 0)))
    - eav(float((campaign.get("baseline") or {}).get("operations_index", 0))), 2
)
if not math.isclose(float(deltas.get("effort_adjusted_value", -1)), expected_delta, abs_tol=0.01):
    errors.append(f"campaign: expected EAV delta {expected_delta}, found {deltas.get('effort_adjusted_value')!r}")

# Ensure scoring contract declares the marginal formula and excludes L-0 from
# maturity resolution.
method_text = " ".join((evaluation.get("method") or {}).get("steps") or [])
if "EAV(S)" not in method_text or "Pk(S) / Mk" not in method_text:
    errors.append("evaluation: marginal-band EAV formula is missing")
if "L-0 is never returned" not in method_text:
    errors.append("evaluation: L-0 exclusion from score-based maturity resolution is missing")

if errors:
    print(f"FAIL — {len(errors)} error(s):")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)

print(
    "OK — maturity-model-operations: manifest + canonical scale + legacy crosswalk + "
    "questionnaire + EAV boundaries + worked examples valid"
)
