# CR-AM-17 — Operations scale identity migration

**Status:** Approved for implementation  
**Date:** 2026-11-23  
**Model:** `dea:maturity-operations`  
**Target release:** `2.1.0`  
**Related:** CR-AM-01 (resolved foundational decision), CR-AM-19 (marginal-band EAV correction)

## 1. Decision

Migrate the Operations Maturity Model from its legacy model-local level identifiers `L0`–`L4` to the canonical v2 level-identification convention:

- `L-0` — Not Assessed (a status/sentinel, not a capability maturity level)
- `L-1` — Emergent
- `L-2` — Structured
- `L-3` — Systematic
- `L-4` — Adaptive
- `L-5` — Self-Optimising

The five Operations-specific names, definitions, characteristics, expected practices, evidence expectations, score ranges and progression semantics are preserved. This change aligns identifiers; it does not replace Operations maturity semantics with another model's labels.

## 2. Compatibility mapping

| Legacy identifier | Canonical identifier | Preserved meaning |
|---|---|---|
| L0 | L-1 | Emergent |
| L1 | L-2 | Structured |
| L2 | L-3 | Systematic |
| L3 | L-4 | Adaptive |
| L4 | L-5 | Self-Optimising |

The mapping is explicit in [`migrations/scale-v1-to-v2-map.yaml`](../../migrations/scale-v1-to-v2-map.yaml). Legacy L0 means Emergent and must never be mapped to the new L-0 Not Assessed sentinel. Historical records retain their original model version and payload; translation is performed only through the published crosswalk. Missing historical criterion records are not automatically synthesized as L-0.

The existing criterion response scores are preserved: legacy L0–L4 and canonical L-1–L-5 map respectively to 0, 25, 50, 75 and 100. L-0 is an explicit unassessed state with score zero and is excluded from the assessed capability-level ladder.

## 3. Canonical band relationship

The Operations Index continues to resolve against the canonical v2 score intervals:

| Score interval | Operations level | Canonical identifier |
|---|---|---|
| 0–20 | Emergent | L-1 |
| 21–45 | Structured | L-2 |
| 46–70 | Systematic | L-3 |
| 71–88 | Adaptive | L-4 |
| 89–100 | Self-Optimising | L-5 |

The scale's effort multipliers remain 1.0, 1.5, 2.5, 4.0 and 6.0. Score aggregation, dimension weights, evidence-confidence multipliers and the 0–100 Operations Index are unchanged.

## 4. Record semantics

New 2.1.0 assessment records identify each criterion's `level_id` and `assessment_status`. `L-0` / `not-assessed` is distinct from an assessed `L-1` / `assessed` response. An unassessed criterion contributes zero to aggregation and is not silently omitted. Score-based band resolution returns only L-1 through L-5.

## 5. Release and validation

The migration is released as Operations model 2.1.0 with scale `dea:scale-operations-v2` version 2.0.0. The scale file, model bindings, questionnaire, evaluation method, evidence schema, migration crosswalk, examples, local validator and README are updated together.

Acceptance requires:
- exact canonical identifier set and distinct L-0 sentinel;
- reversible legacy identifier mapping with unchanged numeric response scores;
- unchanged Operations Index and maturity-band resolution for existing scores;
- explicit unassessed behavior;
- successful Level 1 local validation, Level 2 contract conformance and repository-standard CI.

## 6. EAV sequencing

CR-AM-19 is implemented in the same coordinated release after the scale identity decision. It changes only the supplementary EAV calculation to marginal canonical-band contributions. It does not change the Operations Index, score-to-band resolution or maturity level semantics.
