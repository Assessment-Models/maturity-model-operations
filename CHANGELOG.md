# Changelog — maturity-model-operations

All notable changes to this repository are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] — 2026-11-19

Enterprise expansion of the model (CR-AM-13): from technology-operations
(incident response, observability, deployment automation, SLOs and SRE
practice) to full enterprise operations — the day-to-day activities that
leverage key organizational capabilities to deliver outcomes, anchored in the
operating blueprint, with the Handshake & Touchpoint Model linking sibling
assessment models across the ecosystem.

### Added

- **CR-AM-13 (Phases 0-2)**: enterprise scope definition — change request
  (`docs/cr/CR-AM-13-operations-maturity-v2.md`) defining the six-dimension
  scope (Value-Stream & Daily Operations, Capability Orchestration, Service &
  Process Management, Workforce & Ways of Working, Technology & Infrastructure
  Operations, Strategy Alignment & Operating Blueprint), the normative
  boundary/ownership table, and the Handshake & Touchpoint Model.
- **CR-AM-13 Phase 1**: v2 criteria register
  (`maturity/model/operations-v2-draft.yaml`) — **6 dimensions, 19
  sub-dimensions, 51 criteria** with v1.0.0 lineage flags (this final count
  supersedes the provisional 18/45 noted while the phase was in flight) — plus
  the assessment questionnaire (`maturity/assessment-questionnaire.yaml`),
  one entry per criterion with evidence prompts. Criterion IDs
  (`OPS-D#-SD#-C##`) are permanent benchmarking keys; ID numbering is
  deliberately non-contiguous so future insertions never renumber existing
  criteria.
- **CR-AM-13 Phase 2**: `touchpoints.yaml` — reconciled handshakes and six
  peer touchpoint records (autonomous-operations; digital-transformation
  (composite); digital-transformation-operationalized; modernization;
  services-delivery; technology). Mirror records merged in the four peer
  repositories with published registers; services-delivery and technology
  criterion bindings seeded from their register drafts (PRs
  `maturity-model-services-delivery#4` and `maturity-model-technology#4`,
  seed-pending-release until those peers merge and tag). Version 0.2.0;
  remains `status: draft` until `maturity-touchpoint-contract` publishes in
  `technehub-labs/dea-metamodel` (issue #213).
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

### Changed

- Repository `VERSION` and `model.yaml` bumped 1.0.0 → 2.0.0 (major:
  breaking scope expansion of the assessed domain). `model.yaml` description
  now states the enterprise-operations scope and declares the touchpoints
  manifest.
- Criteria register, assessment questionnaire, evaluation model and evidence
  schema promoted from draft to **stable** at release (register 2.0.0,
  questionnaire 1.0.0, evaluation 1.0.0, evidence schema 1.0.0). The register
  filename retains the `-draft` suffix from Phase 1; renaming is owner
  cleanup and does not affect any contract, criterion ID or record.

### Compatibility

- Criterion IDs are permanent benchmarking keys; 1.x assessment records
  convert via `migrations/v1-to-v2-map.yaml` (v1.0.0 scale items map to
  D5/D4/D6 criteria; D1–D3 are additive and score only from v2.0.0
  campaigns). Assessment records carry the model version used.
- Metamodel compatibility range unchanged (`>=1.0.0 <2.0.0`); scoring
  handshake unchanged (`dea:maturity-bands-v2@v1.0.0`).

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
