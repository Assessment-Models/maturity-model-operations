#!/usr/bin/env python3
"""Level 1 local validation for the Operations Maturity Model (v3, CR-OM-01).

Validates canonical scale identity and legacy crosswalk (CR-AM-17), marginal-band
EAV (CR-AM-19), the v3 enterprise-operations register (nine dimensions, dual
perspectives), questionnaire/evidence/touchpoint/migration resolution, version
coherence, and the worked example + campaign math. Exits non-zero and lists every
detected failure.
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []

V3_VERSION = "3.0.0"
CRITERION_ID = re.compile(r"^OPS-D0[1-9]-SD0[1-9]-C[0-9]{2}$")


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
evaluation = load("maturity/evaluation.yaml")
questionnaire = load("maturity/assessment-questionnaire.yaml")
evidence_schema = load("maturity/evidence/schema.yaml")
touchpoints = load("touchpoints.yaml")
blueprint = load("maturity/blueprint-deduction.yaml")
scale_migration = load("migrations/scale-v1-to-v2-map.yaml")
register_migration = load("migrations/v2-to-v3-map.yaml")
example = load("examples/operations-2026.yaml")
campaign = load("campaigns/baseline-vs-target-2026.yaml")

# Manifest and handshake.
for key in ("id", "type", "name", "version", "conformance"):
    if key not in manifest:
        errors.append(f"model.yaml: missing required field {key}")
if manifest.get("type") not in ("maturity-model", "assessment-model", "assessment-tool"):
    errors.append(f"model.yaml: invalid type {manifest.get('type')!r}")
version_file = ROOT / "VERSION"
if not version_file.is_file():
    errors.append("VERSION: missing release version file")
else:
    declared_version = version_file.read_text().strip()
    if manifest.get("version") != declared_version:
        errors.append(
            f"model.yaml: version {manifest.get('version')!r} does not match "
            f"VERSION {declared_version!r}"
        )
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
if scale.get("version") != V3_VERSION:
    errors.append(f"scale: version must be {V3_VERSION}")
if scale.get("ordering") != "ascending":
    errors.append("scale: ordering must be ascending")
if (scale.get("progression") or {}).get("effort_multiplier") != {
    "L-1": 1.0, "L-2": 1.5, "L-3": 2.5, "L-4": 4.0, "L-5": 6.0
}:
    errors.append("scale: effort multipliers do not match canonical v2 values")
sentinel = next((x for x in levels if x.get("id") == "L-0"), {})
if "not a capability level" not in str(sentinel.get("definition", "")).lower():
    errors.append("scale: L-0 must be explicitly defined as a non-capability sentinel")

# v3 register: identity, nine dimensions, dual perspectives.
if register.get("repo_id") != manifest.get("id"):
    errors.append("register: repo_id does not match model manifest")
if register.get("scale_levels") != ["L-1", "L-2", "L-3", "L-4", "L-5"]:
    errors.append("register: scale_levels must reference L-1..L-5 only")
if register.get("unassessed_level") != "L-0":
    errors.append("register: unassessed_level must be L-0")
scale_ref = register.get("scale_reference") or {}
if scale_ref.get("id") != "dea:scale-operations-v2" or scale_ref.get("version") != V3_VERSION:
    errors.append("register: missing canonical Operations scale reference at the release version")
perspectives = register.get("perspectives") or []
if [p.get("id") for p in perspectives if isinstance(p, dict)] != ["current-realization", "future-readiness"]:
    errors.append("register: perspectives must declare current-realization and future-readiness")
dims, sds, crits = [], {}, {}
for dim in register.get("dimensions", []) or []:
    dims.append(dim.get("id"))
    for sd in dim.get("sub_dimensions", []) or []:
        sds[sd.get("id")] = dim.get("id")
        for c in sd.get("criteria", []) or []:
            crits[c.get("id")] = c
if len(dims) != 9:
    errors.append(f"register: expected 9 dimensions (D01..D09), found {len(dims)}")
if len(crits) < 120:
    errors.append(f"register: expected >=120 criteria, found {len(crits)}")
weights = {d.get("id"): d.get("weight") for d in register.get("dimensions", []) or []}
if abs(sum(w for w in weights.values() if w is not None) - 1.0) > 0.001:
    errors.append("register: dimension weights must sum to 1.00")
for cid, c in crits.items():
    if not CRITERION_ID.match(cid or ""):
        errors.append(f"register: criterion id {cid!r} violates the OPS-D0#-SD0#-C## pattern")
    for field in ("statement", "intent", "current_expectation", "future_expectation", "evidence", "indicators"):
        if not c.get(field):
            errors.append(f"register: criterion {cid} missing {field}")
if len(crits) != len(set(crits)):
    errors.append("register: duplicate criterion ids")

# Evidence schema: criterion pattern, assessment-status semantics.
pattern = ((evidence_schema.get("evidence_item") or {}).get("fields", {}).get("criterion", {}) or {}).get("pattern")
if not pattern:
    errors.append("evidence schema: evidence_item.fields.criterion.pattern is required")
else:
    rx = re.compile(pattern)
    unmatched = [cid for cid in crits if not rx.match(cid)]
    if unmatched:
        errors.append(f"evidence schema: pattern {pattern!r} rejects {len(unmatched)} register ids (e.g. {unmatched[0]})")
record_schema = evidence_schema.get("assessment_record") or {}
score_entry = record_schema.get("criterion_score") or {}
if score_entry.get("required") != ["level_id", "assessment_status", "score", "evidence_confidence"]:
    errors.append("evidence schema: criterion_score required fields are incomplete")
score_rules = score_entry.get("rules") or []
if not any("L-0 requires" in str(rule) and "unverified" in str(rule) for rule in score_rules):
    errors.append("evidence schema: L-0 must require not-assessed, score 0 and unverified confidence")
if not any("legacy L0" in str(rule) and "L-1" in str(rule) for rule in score_rules):
    errors.append("evidence schema: legacy L0 must be distinguished from canonical L-0")
dual = record_schema.get("dual_perspective_score") or {}
if dual.get("required") != ["current", "future"]:
    errors.append("evidence schema: dual_perspective_score must require current and future entries")

# Questionnaire: response scale, perspectives, coverage identity.
response_scale = questionnaire.get("response_scale") or {}
if response_scale.get("assessed_levels") != ["L-1", "L-2", "L-3", "L-4", "L-5"]:
    errors.append("questionnaire: assessed_levels must be L-1..L-5")
if response_scale.get("unassessed_level") != "L-0":
    errors.append("questionnaire: unassessed_level must be L-0")
if response_scale.get("score_mapping") != {
    "L-1": 0, "L-2": 25, "L-3": 50, "L-4": 75, "L-5": 100
}:
    errors.append("questionnaire: score mapping is incorrect")
for p in ("current-realization", "future-readiness"):
    if p not in (questionnaire.get("perspectives") or []):
        errors.append(f"questionnaire: perspectives must include {p}")
q_ids = [e.get("criterion") for e in questionnaire.get("entries", []) or [] if isinstance(e, dict) and e.get("criterion")]
if sorted(q_ids) != sorted(crits):
    missing = set(crits) - set(q_ids)
    extra = set(q_ids) - set(crits)
    errors.append(f"questionnaire: ids do not match register (missing {len(missing)}, extra {len(extra)})")

# Touchpoints resolve into the register (one criterion may feed several peers).
tp_pairs = set()
declared_count = 0
for tp in touchpoints.get("touchpoints", []) or []:
    if not (tp.get("peer_touchpoint_id") and tp.get("mirrors")):
        errors.append(f"touchpoints: {tp.get('id')} is missing peer_touchpoint_id/mirrors")
    for m in tp.get("criteria_mapping", []) or []:
        ours = m.get("ours")
        declared_count += 1
        pair = (tp.get("id"), ours)
        if pair in tp_pairs:
            errors.append(f"touchpoints: {tp.get('id')} maps {ours!r} more than once")
        tp_pairs.add(pair)
        if ours not in crits:
            errors.append(f"touchpoints: {tp.get('id')} maps unknown criterion {ours!r}")

# Blueprint deduction rules resolve.
for rule in blueprint.get("rules", []) or []:
    for sd_id in ((rule.get("when") or {}).get("dims") or {}):
        if sd_id not in sds:
            errors.append(f"blueprint: rule {rule.get('id')} references unknown sub-dimension {sd_id!r}")
    gap_rule = (rule.get("when") or {}).get("gap")
    if gap_rule and gap_rule.get("rule") != "readiness < current":
        errors.append(f"blueprint: rule {rule.get('id')} has an unrecognized gap rule")

# Legacy compatibility map: L0 is Emergent, not the new L-0 sentinel.
legacy = ((scale_migration.get("mapping") or {}).get("legacy_levels") or {})
if legacy != {"L0": "L-1", "L1": "L-2", "L2": "L-3", "L3": "L-4", "L4": "L-5"}:
    errors.append(f"scale migration: unexpected legacy level mapping {legacy!r}")
unassessed = ((scale_migration.get("mapping") or {}).get("new_unassessed_state") or {})
if unassessed.get("id") != "L-0" or unassessed.get("legacy_equivalent") is not None:
    errors.append("scale migration: L-0 must have no legacy equivalent")
if scale_migration.get("status") != "stable":
    errors.append("scale migration: scale crosswalk must be stable")

# Register migration: all 51 v2 criteria re-homed into the v3 register.
migration_from = [m.get("from") for m in register_migration.get("criterion_map", []) or [] if not m.get("secondary")]
migration_to = [m.get("to") for m in register_migration.get("criterion_map", []) or []]
if len(set(migration_from)) != 51:
    errors.append(f"register migration: expected 51 primary v2 criterion mappings, found {len(set(migration_from))}")
for to in migration_to:
    if to not in crits:
        errors.append(f"register migration: target {to!r} does not exist in the v3 register")

# Version coherence across the declared artifacts.
readme_text = (ROOT / "README.md").read_text() if (ROOT / "README.md").is_file() else ""
std = load("standard.yaml") or {}
std_version = ((std.get("model") or {}).get("version") or "").strip()
manifest_version = ""
try:
    manifest_version = json.loads((ROOT / "assessment-manifest.json").read_text()).get("version", "")
except (OSError, ValueError):
    errors.append("assessment-manifest.json: not valid JSON")
for where, v in {
    "standard.yaml": std_version,
    "assessment-manifest.json": (manifest_version or "").lstrip("v"),
    "register": register.get("version"),
    "evaluation.model_version": evaluation.get("model_version"),
    "questionnaire.model_version": questionnaire.get("model_version"),
}.items():
    if v != V3_VERSION:
        errors.append(f"version coherence: {where} is {v!r}, expected {V3_VERSION!r}")
if f"release: {V3_VERSION}" not in readme_text:
    errors.append(f"version coherence: README status line does not state {V3_VERSION!r}")
if register.get("score_scheme") != "dea-maturity-v2" or (register.get("band_reference") or {}).get("id") != "dea:maturity-bands-v2":
    errors.append("register: score_scheme/band_reference must bind dea:maturity-bands-v2")
if evaluation.get("dimension_weights") != weights:
    errors.append("evaluation: dimension_weights differ from the register weights")
for p in ("current-realization", "future-readiness"):
    if p not in (evaluation.get("perspectives") or []):
        errors.append(f"evaluation: perspectives must include {p}")

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

# Ensure the scoring contract declares score preservation, the marginal formula
# and excludes L-0 from maturity resolution.
method_text = " ".join((evaluation.get("method") or {}).get("steps") or [])
if "EAV(S)" not in method_text or "Pk(S) / Mk" not in method_text:
    errors.append("evaluation: marginal-band EAV formula is missing")
if "L-0 is never returned" not in method_text:
    errors.append("evaluation: L-0 exclusion from score-based maturity resolution is missing")
if "0, 25, 50, 75, 100" not in method_text:
    errors.append("evaluation: CR-AM-17 score preservation mapping is missing")
if "future readiness" not in method_text or "Transformation Gap" not in method_text:
    errors.append("evaluation: dual-perspective steps are missing")


def check_index_view(name, view):
    """Weighted index, band/level resolution, marginal EAV, readiness/gap fields."""
    ds = view.get("dimension_scores") or {}
    if set(ds) != set(dims):
        errors.append(f"{name}: dimension_scores keys {sorted(ds)} != register dimensions {sorted(dims)}")
        return None
    expected_index = sum(float(ds[d]) * float(weights[d]) for d in dims if d in ds)
    idx = view.get("operations_index")
    if not isinstance(idx, (int, float)):
        errors.append(f"{name}: operations_index must be numeric")
        return None
    if abs(float(idx) - round(expected_index, 1)) > 0.06:
        errors.append(f"{name}: operations_index {idx} != weighted dimension sum ({round(expected_index, 2)})")
    if not (0 <= float(idx) <= 100):
        errors.append(f"{name}: operations_index {idx} outside [0, 100]")
        return None
    resolved = resolve_band(float(idx))
    if not resolved:
        errors.append(f"{name}: operations_index {idx} resolves to no canonical band")
        return None
    band_id, level_id = resolved
    if view.get("resolved_band") != band_id:
        errors.append(f"{name}: resolved_band {view.get('resolved_band')!r} != computed {band_id!r}")
    if view.get("resolved_level") != level_id:
        errors.append(f"{name}: resolved_level {view.get('resolved_level')!r} != computed {level_id!r}")
    expected_eav = round(eav(float(idx)), 2)
    if not math.isclose(float(view.get("effort_adjusted_value", -1)), expected_eav, abs_tol=0.01):
        errors.append(f"{name}: expected marginal EAV {expected_eav}, found {view.get('effort_adjusted_value')!r}")
    readiness = view.get("readiness_index")
    gap = view.get("transformation_gap")
    if readiness is not None and gap is not None:
        if abs(float(gap) - (float(readiness) - float(idx))) > 0.06:
            errors.append(f"{name}: transformation_gap {gap} != readiness_index - operations_index")
    return float(idx)


# Worked example.
check_index_view("example", example)
for sample in example.get("criterion_score_samples", []) or []:
    for side in ("current", "future"):
        level_id = ((sample.get(side) or {}).get("level_id"))
        if level_id not in {b[4] for b in BANDS} | {"L-0"}:
            errors.append(f"example: sample {sample.get('criterion')} has invalid {side} level {level_id!r}")
    if ((sample.get("current") or {}).get("level_id") == "L-0") and (
        (sample.get("current") or {}).get("assessment_status") != "not-assessed"
        or float((sample.get("current") or {}).get("score", -1)) != 0
        or (sample.get("current") or {}).get("evidence_confidence") != "unverified"
    ):
        errors.append(f"example: sample {sample.get('criterion')} violates the L-0 not-assessed rules")

# Campaign examples and deltas.
for key in ("baseline", "target"):
    record = campaign.get(key) or {}
    if not record:
        errors.append(f"campaign: missing {key}")
        continue
    check_index_view(f"campaign.{key}", record)
if campaign.get("baseline") and campaign.get("target"):
    b, t = campaign["baseline"], campaign["target"]
    for d in dims:
        bd = (b.get("dimension_scores") or {}).get(d)
        td = (t.get("dimension_scores") or {}).get(d)
        delta = ((campaign.get("deltas") or {}).get("dimensions") or {}).get(d)
        if None not in (bd, td, delta) and abs(float(delta) - (float(td) - float(bd))) > 0.01:
            errors.append(f"campaign.deltas.dimensions[{d}] is {delta}, expected {float(td) - float(bd):.1f}")
    for field in ("operations_index", "readiness_index"):
        d = (campaign.get("deltas") or {}).get(field)
        if d is not None and abs(float(d) - (float(t[field]) - float(b[field]))) > 0.06:
            errors.append(f"campaign.deltas.{field} is {d}, expected {float(t[field]) - float(b[field]):.2f}")
    d_gap = (campaign.get("deltas") or {}).get("transformation_gap")
    if d_gap is not None:
        expected_gap_delta = float(t.get("transformation_gap", 0)) - float(b.get("transformation_gap", 0))
        if abs(float(d_gap) - expected_gap_delta) > 0.06:
            errors.append(f"campaign.deltas.transformation_gap is {d_gap}, expected {expected_gap_delta:.2f}")
    d_eav = (campaign.get("deltas") or {}).get("effort_adjusted_value")
    if d_eav is not None:
        expected_delta = round(eav(float(t["operations_index"])) - eav(float(b["operations_index"])), 2)
        if not math.isclose(float(d_eav), expected_delta, abs_tol=0.01):
            errors.append(f"campaign: expected EAV delta {expected_delta}, found {d_eav!r}")

if errors:
    print(f"FAIL — {len(errors)} error(s):")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)

print(
    f"OK — maturity-model-operations v{V3_VERSION}: manifest + canonical scale + legacy crosswalk + "
    f"v3 register ({len(dims)} dimensions, {len(crits)} criteria, dual perspectives) + evaluation "
    f"(score preservation + marginal EAV) + questionnaire + evidence + touchpoints "
    f"({declared_count} mappings) + blueprint + register migration (51 v2 criteria) + "
    f"EAV boundaries + worked examples valid"
)
