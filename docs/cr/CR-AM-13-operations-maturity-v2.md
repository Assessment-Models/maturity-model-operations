# CR-AM-13 — Operations Maturity Model Enterprise Expansion & Ecosystem Handshake

> Draft change request for review. Status: draft. Date: 2026-11-19.
> Umbrella: CR-AM-01. Related: CR-AM-11, CR-AM-12, CR-AM-ORG-RES-000, CR-AR-01.
> Target: `dea:maturity-operations` release line `2.0.0` (non-breaking for 1.x assessment records).

## §1 Problem statement

`dea:maturity-operations` v1.0.0 assesses **technology operations only** (incident response, observability, deployment automation, SLO/SRE). The intended purpose is broader: operations as the **operating engine of the enterprise** — day-to-day activities that leverage organizational capabilities to deliver outcomes and drive strategy.

Four gaps block that intent:

1. **Scope gap** — no representation of value-stream operations, capability orchestration, service/process management, workforce operations, or strategy linkage.
2. **Isolation gap** — no declared handshake or touchpoints with sibling models; `maturity-model-autonomous-operations` already contains an Operations dimension (4.x) whose criteria explicitly source this model (3.3.8 Observability & Event Intelligence; 4.2.5 SLO & Error Budget Management), and `maturity-model-digital-transformation-operationalized` publishes an Operations dimension (d4) overlapping our D5 evidence.
3. **Instrument gap** — no criteria register, questionnaire, or evidence-collection structure; only a 5-level scale and an illustrative worked example.
4. **Living-program gap** — no evidence schema, no repeat-assessment/benchmarking format, no version-compatibility rules for assessment results across model versions.

## §2 Objectives

- Elevate the model from technology-ops to enterprise operations (the "oil of the operating blueprint").
- Absorb, not discard, v1.0.0 content (benchmarking continuity).
- Introduce a machine-checkable **Handshake & Touchpoint Model** with sibling models.
- Make the model a living program: evidence-backed assessments, benchmark deltas, versioned compatibility.
- Keep ecosystem invariants: independent versioning, CR-AM-11 §15 contract handshake, registry registration, three CI levels, AM-MODEL-REPOSITORY-STANDARD conformance.

**Non-goals:** redefining the metamodel, subsuming sibling models, new scoring bands (canonical v2 bands retained), git submodules (prohibited by CR-AM-11 §23).

## §3 Revised scope — enterprise operations

Operations is assessed as the enterprise's operating-engine layer: how the organization runs day-to-day, anchors on key capabilities, and converts strategy into outcomes. The nexus of digital forces (AI, automation, data, platforms, people, process) is a first-class operating condition.

| Dim | Name | Weight | Assesses |
|---|---|---|---|
| D1 | Value-Stream & Daily Operations | 20% | Daily work flows through value streams, made visible and managed to commitments |
| D2 | Capability Orchestration | 18% | Discovering, leveraging and coordinating key capabilities to deliver outcomes |
| D3 | Service & Process Management | 18% | Standardization, ownership, service quality (SLAs/OLAs), continual improvement |
| D4 | Workforce & Ways of Working | 14% | Operating roles, team topologies, skills, sustainability of cadence |
| D5 | Technology & Infrastructure Operations | 20% | Observability, incident/problem management, deployment/change automation, reliability (SLO/SRE) — absorbs all v1.0.0 content |
| D6 | Strategy Alignment & Operating Blueprint | 10% | Strategy-to-operations linkage, operating-model governance, digital-nexus adoption |

## §4 Boundary resolution (overlap table)

| Subject | Owning model | Relationship from operations model |
|---|---|---|
| Human/assisted enterprise operations | **this model** | Owns D1–D4, D6 |
| Tech & infra operations (run, monitor, deploy, SRE) | **this model** | Owns D5 (absorbs v1.0.0) |
| Closed-loop autonomous operations (OODA, agent governance) | `maturity-model-autonomous-operations` | Touchpoint: D5 evidence feeds register criteria 3.3.8, 4.1.x, 4.2.5; level split at auto-remediation → autonomy |
| Delivery flow, time-to-market, customer outcomes | `maturity-model-services-delivery` | Touchpoint: D1 outcomes state; no duplicate criteria (peer register pending) |
| Platforms, tools, technology capability | `maturity-model-technology` | Touchpoint: D5 consumes platform capability; assesses tool-use effectiveness only (peer register pending) |
| Transformation strategy, TOM design, transformation execution | `maturity-model-digital-transformation` + `-operationalized` | Touchpoint: D6 consumes strategy state (d2c1); TOM design owned by peer (d5c2); shared d4 evidence single-assessed |
| Architecture modernization practice | `maturity-model-modernization` | Touchpoint: shared `operations-modernization` component; peer catalog (execution-operations) is complementary |

Rule: **one criterion has one owning model.** Sibling coverage is via touchpoint mapping, never duplication.

## §5 Handshake & Touchpoint Model (normative)

- **Handshake** (contractual): pinned, immutable contract-level linkage — contract id + version, direction, peer asset id, validated by ecosystem CI against the registry.
- **Touchpoint** (semantic seam): a concrete meet-point where two models exchange meaning during an assessment, living in `touchpoints.yaml` with criteria mappings on both sides and an overlap-resolution note.

Evidence of pre-existing reciprocity: the Autonomous Operations register already declares a `derived-from` (`extends`) relationship to `dea:maturity-operations`, and its added criteria 3.3.8 and 4.2.5 are sourced from this model. The mirrored touchpoint formalizes it.

Record fields: `id`, `peer_asset`, `peer_contract_version`, `direction`, `mapping_type` (feeds/consumes/shared-component/boundary), `criteria_mapping`, `overlap_resolution`, `reciprocity`, `peer_status`.

Enforcement: `assessment-ci` gains a touchpoint-reciprocity check (soft-fail warning for 90 days, then hard-fail); Level 3 ecosystem CI validates touchpoint records against the registry on every PR. A `maturity-touchpoint-contract` (v0.1-draft, then 1.0 after ≥3 adopters) is proposed for publication in `technehub-labs/dea-metamodel`.

## §6 Living-program mechanics

- **Evidence schema** (`maturity/evidence/schema.yaml`): artifact references, collection dates, confidence per criterion; assessments become auditable and comparable.
- **Assessment campaign records**: baseline → target with a delta format (per-dimension deltas, band transitions, effort-adjusted value change).
- **Version compatibility rules** (`model.yaml`): criterion IDs are permanent keys; assessment records remain benchmarkable across 1.x/2.x while `migrations/v1-to-v2-map.yaml` carries lineage; breaking ID changes require a minor-model-version bump and published migration map.
- **Blueprint deduction** (`maturity/blueprint-deduction.yaml`, Phase 3): rule map from gap patterns to operational-blueprint recommendations.
- **Dual cadence**: model SemVer for content; campaign records form the benchmarking time-series independent of model releases.

## §7 Phasing & exit criteria

| Phase | Deliverable | Exit criterion |
|---|---|---|
| 0 — Decisions | This CR approved; touchpoint contract v0.1 agreed with `technehub-labs` and sibling owners | CR merged; contract draft published |
| 1 — Restructure | Criteria register (`maturity/model/operations-v2-draft.yaml`), `evaluation.yaml`, questionnaire, migration map | Level 1–2 CI green; every v1.0.0 scale item mapped |
| 2 — Handshake | `touchpoints.yaml` for six peers; mirrored records in peer repos; CI reciprocity check | Peers merge mirrored records; Level 3 CI green |
| 3 — Living program | Evidence schema; campaign/benchmark formats; blueprint-deduction rules | One worked end-to-end campaign validated |
| 4 — Ecosystem wiring | Registry records updated (incl. `compatibility/`); portal drill-down; template updated with touchpoint convention | Registry merge; portal live |

## §8 Risks & mitigations

| Risk | Mitigation |
|---|---|
| Peer repos stall on reciprocity | Soft-fail warning for 90 days, then hard-fail |
| Scope creep into sibling territory | §4 ownership table is normative; CI blocks criteria colliding with mapped peer criteria |
| Benchmark discontinuity with v1.0.0 | Migration map; D5 dimension score convertible to legacy scale |
| Touchpoint contract churn | Starts 0.1-draft, pinned per-repo, promoted to 1.0 only after ≥3 models adopt |

## §9 Decisions requested

1. Approve the six-dimension enterprise scope (§3) and the boundary table (§4).
2. Approve the Handshake & Touchpoint Model as an ecosystem standard candidate (§5).
3. Approve model release line `2.0.0-rc` → `2.0.0` with 1.x assessment compatibility (§6).
4. Nominate owners for the reciprocal touchpoint records in the six peer repositories.
