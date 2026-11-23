# Changelog — maturity-model-operations

## [Unreleased]

### [3.0.0] — CR-OM-01: Enterprise Operations v3 (release prepared; tagging gated on dea-metamodel #214 ratification)

Evolution of the model into the parent operational assessment for enterprise
operations, from CR-Operations-00000 (domain foundation) and
CR-Model-Assessment-Operations-0001 (evolution architecture), rebased on the
approved CR-AM-17 scale identity migration and CR-AM-19 marginal-band EAV.
Full programme: `docs/cr/CR-OM-01-enterprise-operations-v3.md`.

### Added

- **Nine-dimension enterprise-operations taxonomy** — D01 Operating Model,
  D02 Operational Capabilities, D03 Value Streams & Processes, D04 Service &
  Delivery Management, D05 People & Organization, D06 Resources & Assets,
  D07 Information & Technology, D08 Operational Governance & Resilience,
  D09 Operational Performance & Value. **44 sub-dimensions, 132 criteria**
  (`OPS-D01-SD01-C01` … `OPS-D09-SD04-C03`), each carrying `statement`,
  `intent`, `current_expectation`, `future_expectation`, `evidence` and
  `indicators`.
- **Dual assessment perspectives** — Current Operational Realization and
  Future Operational Readiness scored on every criterion without collapsing
  into one number; derived **Readiness Index** and **Transformation Gap**
  (readiness − maturity, per dimension and overall). Four assessment result
  views: current maturity (Operations Index + band + resolved level),
  performance & value (efficiency/effectiveness read separately from
  enterprise value realization), future readiness, transformation gap.
- **Additive progression vocabulary** `ops_stage_by_ordinal` on the register
  (Absent, Initial, Defined & Managed, Integrated, Adaptive) — metadata,
  never a second level ladder.
- `migrations/v2-to-v3-map.yaml` — all 51 v2 criterion ids → v3 homes; scale
  identifiers and criterion scores are handled by (and preserved through) the
  CR-AM-17 crosswalk; evidenced-absence and no-synthesized-L-0 rules.
- `docs/domain/enterprise-operations.md` — authoritative domain definition,
  boundaries, assessment lenses, method and constructs.
- `docs/cr/CR-OM-01-enterprise-operations-v3.md` — the change programme
  (reconnaissance, decisions, architecture, reconciliation with CR-AM-17/19,
  phases, ecosystem dependencies, risks).
- Blueprint-deduction rules for resilience, value realization and the
  transformation gap (`bp-continuity-resilience`, `bp-value-realization`,
  `bp-readiness-closure`).

### Changed

- **Level semantics evolve to enterprise operations** (deliberate
  major-boundary decision, CR-OM-01 §5a): the CR-AM-17 preserve-verbatim
  choice is superseded for v3 — level definitions/characteristics are
  rewritten from technology-operations wording to enterprise operations per
  CR-Operations-00000, while the identifier migration, level names, score
  bands and criterion score preservation (0/25/50/75/100) are unchanged.
  L-5 explicitly does NOT require autonomous execution. Renumbering
  adoption remains annotated pending dea-metamodel #214 ratification.
- **BREAKING — criterion/dimension re-identification**: v2 D1..D6 map into
  D01..D09; all 51 v2 criterion ids resolve through the migration map (v2 ids
  remain resolvable benchmarking keys; 81 criteria are new and score only
  from v3.0.0 campaigns).
- Criteria register consolidated: `maturity/model/operations.yaml` becomes
  the single v3 register (supersedes the v1 identity register at that path
  and removes `operations-v2-draft.yaml` — the -draft rename recorded as
  owner cleanup in the 2.0.0 CHANGELOG; 2.1.x additions — `scale_reference`,
  `unassessed_level`, crosswalk pointer — are folded in).
- `maturity/evaluation.yaml`: perspectives steps, Readiness Index,
  Transformation Gap and the four result views added on top of the preserved
  CR-AM-17 score mapping and CR-AM-19 marginal-band EAV formula;
  `level_band_map` binding retained; band definitions referenced by id, not
  restated in prose.
- Questionnaire regenerated (132 dual-perspective entries) with the
  `response_scale` contract (assessed levels L-1..L-5, unassessed L-0,
  score mapping 0/25/50/75/100).
- Evidence schema: criterion pattern `OPS-D0[1-9]-SD0[1-9]-C[0-9]{2}`;
  per-perspective `criterion_score` records (2.1.0 structure preserved:
  `level_id` / `assessment_status` / `score` / `evidence_confidence` with the
  L-0 and legacy-L0 rules) composed as `current` + `future`; derived results
  extended with the four views.
- Touchpoints v0.3.0: every `ours:` mapping re-pointed to v3 criterion ids
  (v2 ids noted inline); the reciprocal `peer_touchpoint_id` / `mirrors` /
  `reciprocity` declarations and the corrected AO root-cause mapping
  (OPS-D5-SD2-C05 → v3 OPS-D08-SD05-C03) are preserved; specialization rule
  recorded (parent assesses governance/integration of autonomous execution,
  AO peer assesses its depth; no cross-model score averaging); peer statuses
  → `peer-remap-pending` pending the reciprocity wave.
- Worked example and campaign recomputed under v3 (nine dimensions, dual
  perspectives, marginal-band EAV); campaign re-pinned `@3.0.0`.
- `model.yaml` 3.0.0 with the parent-assessment description; VERSION,
  `standard.yaml` and `assessment-manifest.json` aligned at 3.0.0; manifest
  gains nine dimension names, perspectives and a scale block.
- `scripts/local_validate.py` extended on the 2.1.x rewrite: adds v3 register
  taxonomy and dual-perspective field checks, questionnaire/evidence/
  touchpoint/migration resolution, version coherence across VERSION /
  model.yaml / standard.yaml / manifest / README, worked-example weighting
  and campaign delta checks — retaining the canonical scale, crosswalk and
  marginal-EAV boundary checks.
- README reworked on the reader-first structure: nine-dimension table, dual
  perspectives and the four result views, enterprise-operations level
  semantics with the ops-stage vocabulary, updated boundaries (parent vs
  specialized models), repository contents and 3.0.0 status.

### Compatibility

- Criterion IDs are permanent benchmarking keys: 1.x records convert via
  `migrations/v1-to-v2-map.yaml`; 2.x records convert via
  `migrations/v2-to-v3-map.yaml`; legacy scale identifiers translate only
  through `migrations/scale-v1-to-v2-map.yaml` (legacy L0 → L-1, never L-0).
  Criterion response scores are preserved throughout (0/25/50/75/100).
- Evidenced absence scores L-1; L-0 is reserved exclusively for "not
  assessed" and is never synthesized for missing legacy records.
- Operations Index and band/level resolution semantics are unchanged by v3
  itself; historical indexes re-aggregate only through the dimension/criterion
  re-homing and the v3 weights.
- Metamodel compatibility range unchanged (`>=1.0.0 <2.0.0`); scoring
  handshake unchanged (`dea:maturity-bands-v2@v1.0.0`).
- Gateway rendering of the six-level ladder is supported by the
  convention-agnostic engine (levels fix merged).

### Changed (pre-v3, on main)

- **CR-AM-13 Phase 2 reconciliation**: make all six Operations touchpoint relationships explicitly reciprocal with peer touchpoint IDs, mirror IDs and directional reciprocity declarations. Preserve each model's assessment ownership and the draft touchpoint-contract status.
- Correct the Autonomous Operations root-cause mapping to `OPS-D5-SD2-C05` (problem management); `OPS-D5-SD2-C03` remains the distinct incident-command criterion.


All notable changes to this repository are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.1] — 2026-11-23

### Changed

- **CR-AM-13**: add the explicit reciprocal peer-touchpoint identifier and mirror pointer for Autonomous Operations. Preserve the existing evidence mapping, directional ownership boundary and draft contract status; increment the touchpoint artifact version to 0.2.2.

## [2.1.0] — 2026-11-23

### Changed

- **CR-AM-17**: migrate the Operations scale to the canonical L-1..L-5 identifiers and add L-0 Not Assessed as a distinct non-capability state. Preserve the five Operations level names, definitions, score bands and progression semantics. Publish an explicit legacy L0..L4 to L-1..L-5 compatibility map; legacy L0 is never translated to L-0.
- **CR-AM-19**: replace whole-score-times-resolved-band EAV with marginal canonical-band contributions. The Operations Index, dimension weights, evidence-confidence multipliers and maturity-band resolution remain unchanged.
- Update the assessment questionnaire, model register, evidence schema, worked examples, campaign example, local validator and README to the 2.1.0 scale/scoring contract.

### Compatibility

- Existing 2.0.0 assessment records retain their original identifiers and interpretation. Consumers translate legacy scale identifiers only through `migrations/scale-v1-to-v2-map.yaml`.
- New 2.1.0 records use L-0 for Not Assessed and L-1..L-5 for assessed maturity levels. L-0 is never a score-resolved maturity level.
- Operations Index values and canonical band/level resolution are unchanged; EAV values change to the marginal-band method and must not be compared with legacy whole-score-times-multiplier EAV values without recalculation.

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
