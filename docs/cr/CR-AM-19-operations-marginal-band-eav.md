# CR-AM-19 — Operations marginal-band effort-adjusted value

**Status:** Approved for implementation  
**Date:** 2026-11-23  
**Model:** `dea:maturity-operations` 2.1.0  
**Dependency:** CR-AM-17 — canonical scale identity migration

## 1. Decision

Replace the former whole-score-times-resolved-band-multiplier calculation with marginal-band effort-adjusted value (EAV). The Operations Index remains the weighted 0–100 maturity score. Its band and canonical level are resolved independently of EAV.

## 2. Normative formula

For aggregate Operations Index (S), where (0 leq S leq 100):

`EAV(S) = Σ(Pk(S) / Mk)`

- `Pk(S)` is the marginal number of score points from `S` falling within canonical band `k`.
- `Mk` is the effort multiplier for that band.

| Band | Marginal score interval | Multiplier |
|---|---:|---:|
| L-1 Emergent | [0, 20] | 1.0 |
| L-2 Structured | (20, 45] | 1.5 |
| L-3 Systematic | (45, 70] | 2.5 |
| L-4 Adaptive | (70, 88] | 4.0 |
| L-5 Self-Optimising | (88, 100] | 6.0 |

The theoretical maximum is:

`20/1.0 + 25/1.5 + 25/2.5 + 18/4.0 + 12/6.0 = 53.1666666667`

Report EAV to two decimal places. Do not multiply the entire Operations Index by the multiplier of its resolved band.

## 3. Preserved semantics

The correction does not change:
- the Operations Index or its 0–100 range;
- the six dimension weights or aggregation sequence;
- criterion scores or evidence-confidence multipliers;
- canonical score-band boundaries or maturity-level resolution;
- the distinction between L-0 Not Assessed and assessed levels L-1–L-5.

EAV remains supplementary. It is not a maturity score, does not determine the resolved level and is not a financial valuation.

## 4. Worked values

| Operations Index | Marginal calculation | EAV |
|---:|---|---:|
| 62.00 | 20/1.0 + 25/1.5 + 17/2.5 | 43.47 |
| 59.10 | 20/1.0 + 25/1.5 + 14.1/2.5 | 42.27 |
| 67.90 | 20/1.0 + 25/1.5 + 22.9/2.5 | 45.83 |

The campaign example's EAV delta is 3.52. The Operations Index values and resolved levels remain unchanged.

## 5. Validation

Local validation checks the formula at 0, 20, 45, 70, 88 and 100, verifies a score crossing multiple bands, and independently recomputes both worked examples and the campaign delta. Level 1 local CI, Level 2 contract conformance and repository-standard CI must pass.
