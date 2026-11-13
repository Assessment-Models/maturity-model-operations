# Operations Maturity Model

Operations Maturity Model — assesses incident response, observability, deployment automation, SLOs and SRE practice.

## Status

`1.0.0` · stable — canonical v2 bands, independently released

## Placement

This repository is the independent home of the `dea:maturity-operations` maturity
model. Under the Assessment-Models organisation taxonomy (CR-AM-11 §8,
`.github/GOVERNANCE.md`) a maturity model is an independently versioned asset
with its own releases, issues, roadmap and contributors.

Assessment-Models is categorically the home of **capability** assessment
assets. The maturity model for *enterprise architecture practice itself* is
owned by the DEA federation (`technehub-labs`), not by this organisation.

## Scoring scheme

Canonical v2 bands — `dea:maturity-bands-v2` v1.0.0
(`technehub-labs/dea-metamodel`). Non-linear band widths 20/25/25/18/12 with
per-level effort multipliers 1.0 → 6.0:

| Band id | Name | Range | Width | Effort multiplier | Legacy (v1) name |
|---|---|---|---|---|---|
| `level-1-emergent` | Emergent | 0–20 | 21 | 1.0× | Ad Hoc |
| `level-2-structured` | Structured | 21–45 | 25 | 1.5× | Defined |
| `level-3-systematic` | Systematic | 46–70 | 25 | 2.5× | Managed |
| `level-4-adaptive` | Adaptive | 71–88 | 18 | 4.0× | Quantitatively Managed |
| `level-5-self-optimising` | Self-Optimising | 89–100 | 12 | 6.0× | Optimising |

## Layout

```
maturity-model-operations/
├── model.yaml                       # CR-AM-11 §15 contract handshake
├── VERSION
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── maturity/
│   ├── scale.yaml                     # model-owned scale (L0..L4)
│   └── model/operations.yaml
├── examples/
│   └── operations-2026.yaml
├── scripts/
│   └── local_validate.py            # Level 1 validator
└── .github/workflows/
    ├── local-model-ci.yml           # Level 1
    └── contract-conformance.yml     # Level 2 (reusable from assessment-ci)
```

## CI levels

1. **Level 1 — local model CI** (`.github/workflows/local-model-ci.yml`):
   runs `scripts/local_validate.py` — manifest contract, handshake shape,
   scale integrity, register-to-scale resolution, worked-example scoring math
   against the canonical v2 bands.
2. **Level 2 — contract conformance**
   (`.github/workflows/contract-conformance.yml`): reuses
   `Assessment-Models/assessment-ci/.github/workflows/contract-conformance.yml`
   to resolve the §15 handshake against the published contract suite at the
   pinned `dea-metamodel` release.
3. **Level 3 — ecosystem CI**: the registration record in
   `Assessment-Models/assessment-registry` is resolved by the ecosystem
   validator on every registry pull request.

## Provenance

`technehub-labs/dea-metamodel` — `assessment-models/maturity/v2-beta/operations.yaml` (the v2-beta port of the frozen v1-alpha catalog entry).

Level semantics (characteristics, exit criteria, evidence) are carried
**verbatim** from the source; only the scoring fields differ between the
frozen v1-alpha lineage and the canonical v2 scheme.

## Licence

MIT — see `LICENSE`.
