# Changelog — maturity-model-operations

All notable changes to this repository are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **CR-AM-13 (Phases 0-2)**: enterprise expansion of the model — change
  request (`docs/cr/CR-AM-13-operations-maturity-v2.md`) defining the
  six-dimension scope (Value-Stream & Daily Operations, Capability
  Orchestration, Service & Process Management, Workforce & Ways of Working,
  Technology & Infrastructure Operations, Strategy Alignment & Operating
  Blueprint), the normative boundary/ownership table, and the Handshake &
  Touchpoint Model.
- **CR-AM-13 Phase 1**: v2 criteria register draft
  (`maturity/model/operations-v2-draft.yaml`) — 6 dimensions, 18
  sub-dimensions, 45 criteria with v1.0.0 lineage flags — plus the
  assessment questionnaire (`maturity/assessment-questionnaire.yaml`),
  one entry per criterion with evidence prompts.
- **CR-AM-13 Phase 2**: `touchpoints.yaml` — reconciled handshakes and six
  peer touchpoint records (autonomous-operations 3.3.8/4.1.x/3.1.3/4.2.5/3.3.6;
  digital-transformation-operationalized d2c1/d4c2/d4c10/d4c11/d5c2;
  digital-transformation strategy-dimension; modernization
  execution-operations; services-delivery and technology pending peer
  registers). Mirror-record PRs opened in the four peer repositories.
- **CR-AM-13 Phase 3**: evaluation model (`maturity/evaluation.yaml`),
  evidence schema (`maturity/evidence/schema.yaml`), v1-to-v2 migration
  map (`migrations/v1-to-v2-map.yaml`), blueprint-deduction rule map
  (`maturity/blueprint-deduction.yaml`) and a worked campaign example
  (`campaigns/baseline-vs-target-2026.yaml`).
- CR-AM-11 §18–20 (Phase 5): explicit reuse of the `operations-modernization`
  dimension package published in `Assessment-Models/maturity-components`
  (version 1.0.0, immutable reference `v1.0.0`, kind: import). This makes
  `operations-modernization` the first component reused by two independently
  versioned models (`maturity-model-digital-transformation` and this model),
  satisfying the CR-AM-11 Phase 5 exit criterion. The reference carries no
  scoring or scale semantics — those remain owned by this model.

## [1.0.0] — 2026-11-13

### Added

- Initial release of the `dea:maturity-operations` maturity model as an
  independently versioned asset, per the Assessment-Models organisation
  taxonomy (CR-AM-11 §8).
- Model-owned scale conforming to the published `maturity-scale.schema.json`:
  five levels, ordinals 0–4, `ordering: ascending`, linear topology with
  exponential progression, scored against the canonical v2 band instance
  (`dea:maturity-bands-v2` v1.0.0) — non-linear widths 20/25/25/18/12 and
  per-level effort multipliers 1.0 → 6.0.
- CR-AM-11 §15 contract handshake (`model.yaml`) declaring conformance to
  `maturity-scale-contract`, `maturity-model-contract` and
  `conformance-contract` against `technehub-labs/dea-metamodel`.
- Level 1 local model CI and Level 2 contract conformance workflows.
- Worked scoring example demonstrating canonical v2 band resolution and the
  effort-adjusted value.

### Notes

- Level semantics are carried verbatim from the authoritative source; only the
  scoring fields differ between the frozen v1-alpha lineage and the canonical
  v2 scheme.
