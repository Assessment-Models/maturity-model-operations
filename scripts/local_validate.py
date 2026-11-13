#!/usr/bin/env python3
"""Level 1 — local model validation for maturity-model-operations (CR-AM-11 §14).

Checks:
  1. model.yaml parses and matches the Assessment-Models manifest contract
     (`Assessment-Models/assessment-ci/schemas/model-manifest.schema.json`)
  2. the §15 contract handshake is well formed (contract id + version + source)
  3. maturity/scale.yaml declares exactly 5 levels with ordinals 0..4 and the
     expected identifiers, plus a conformant ordering/progression contract
  4. maturity/model/operations.yaml carries the model identity, and its level references
     resolve against the scale
  5. examples/operations-2026.yaml computes correctly: the aggregated score lies in [0, 100],
     the resolved band matches the canonical v2 bands, and the
     effort-adjusted value applies that band's effort multiplier

Exit 0 with OK when clean; exit 1 listing every failure otherwise.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []


def load(rel: str):
    p = ROOT / rel
    if not p.is_file():
        errors.append(f"missing file: {rel}")
        return {}
    return yaml.safe_load(p.read_text()) or {}


manifest = load("model.yaml")
scale = load("maturity/scale.yaml")
register = load("maturity/model/operations.yaml")
example = load("examples/operations-2026.yaml")

# 1 — manifest shape
for key in ("id", "type", "name", "version", "conformance"):
    if key not in manifest:
        errors.append(f"model.yaml: missing required field {key}")
if manifest.get("type") not in ("maturity-model", "assessment-model", "assessment-tool"):
    errors.append(f"model.yaml: invalid type {manifest.get('type')!r}")

# 2 — contract handshake
conf = manifest.get("conformance") or {}
contract = conf.get("contract") or {}
if not contract.get("id"):
    errors.append("model.yaml: conformance.contract.id is required")
if not conf.get("version"):
    errors.append("model.yaml: conformance.version is required")
src = conf.get("source") or {}
if not src.get("organization") or not src.get("repository"):
    errors.append("model.yaml: conformance.source organization+repository are required")

# 3 — scale
EXPECTED_LEVELS = ['L0', 'L1', 'L2', 'L3', 'L4']
levels_actual = scale.get("levels") or []
if len(levels_actual) != len(EXPECTED_LEVELS):
    errors.append(f"scale: expected {len(EXPECTED_LEVELS)} levels, found {len(levels_actual)}")
for i, lvl in enumerate(levels_actual):
    if lvl.get("ordinal") != i:
        errors.append(f"scale: level {i} ordinal is {lvl.get('ordinal')!r}, expected {i}")
    if lvl.get("id") not in EXPECTED_LEVELS:
        errors.append(f"scale: unexpected level id {lvl.get('id')!r}")
    if not lvl.get("name") or not lvl.get("definition"):
        errors.append(f"scale: level {lvl.get('id')} requires name and definition")
if scale.get("ordering") != "ascending":
    errors.append("scale: ordering must be 'ascending'")
prog = scale.get("progression") or {}
if not prog.get("topology") or not prog.get("function"):
    errors.append("scale: progression requires topology and function")

# 4 — register identity + level resolution
if register.get("repo_id") != manifest.get("id"):
    errors.append(
        f"register repo_id {register.get('repo_id')!r} != manifest id {manifest.get('id')!r}"
    )
if not register.get("id"):
    errors.append("register: canonical model id is required")
scale_ids = {l.get("id") for l in levels_actual}
for ref in register.get("scale_levels", []) or []:
    if ref not in scale_ids:
        errors.append(f"register: scale level {ref!r} does not exist in the scale")

# 5 — example scoring math against the CANONICAL v2 bands
V2_BANDS = [('level-1-emergent', (0, 20), 'Emergent', 1.0, 'Ad Hoc'), ('level-2-structured', (21, 45), 'Structured', 1.5, 'Defined'), ('level-3-systematic', (46, 70), 'Systematic', 2.5, 'Managed'), ('level-4-adaptive', (71, 88), 'Adaptive', 4.0, 'Quantitatively Managed'), ('level-5-self-optimising', (89, 100), 'Self-Optimising', 6.0, 'Optimising')]


def band_for(score: float):
    for band_id, rng, name, mult, legacy in V2_BANDS:
        if rng[0] <= score <= rng[1]:
            return band_id, name, mult
    return None, None, None


agg = example.get("aggregated_score")
if not isinstance(agg, (int, float)):
    errors.append("example: aggregated_score must be numeric")
else:
    if not (0 <= agg <= 100):
        errors.append(f"example: aggregated_score {agg} is outside [0, 100]")
    band_id, band_name, mult = band_for(float(agg))
    if band_id is None:
        errors.append(f"example: aggregated_score {agg} resolves to no canonical v2 band")
    else:
        declared = example.get("resolved_band")
        if declared != band_id:
            errors.append(f"example: resolved_band {declared!r} != computed {band_id!r}")
        eav = example.get("effort_adjusted_value")
        if eav is not None and mult is not None:
            expected = round(float(agg) * float(mult), 2)
            if abs(float(eav) - expected) > 0.01:
                errors.append(
                    f"example: effort_adjusted_value {eav} != aggregated_score * "
                    f"effort_multiplier ({expected})"
                )

if errors:
    print(f"FAIL — {len(errors)} error(s):")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print(f"OK — maturity-model-operations: manifest + scale ({len(levels_actual)} levels) + register + example valid")
