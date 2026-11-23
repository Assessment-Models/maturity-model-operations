# CR-OM-01 — Enterprise Operations v3: nine dimensions, dual perspectives, L-0 + L-1..L-5

> Change request, implemented under this branch. Status: implemented (adoption
> of the scale renumbering pending dea-metamodel #214 ratification).
> Date: 2026-11-21. Related: CR-AM-13 (superseded v2 programme, historical),
> CR-Operations-00000 (domain foundation), CR-Model-Assessment-Operations-0001
> (evolution architecture), CR-AM-11, CR-AM-ORG-RES-000, dea-metamodel #213
> (touchpoint contract), dea-metamodel #214 (scale renumbering).
> Target: `dea:maturity-operations` release line `3.0.0` (breaking for 2.x
> criterion ids and level labels; migration maps published for both).

## §1 Problem statement (post-2.0.0 reconnaissance)

CR-AM-13 delivered the enterprise expansion, but the released 2.0.0 state
carried structural debt that blocked the model's intended purpose:

1. **Presentation/scope disconnect** — `model.yaml`, the register and the
   manifest declared enterprise operations, while the README still stated the
   v1.0.0 technology-operations scope at `1.0.0 · stable`, and the scale's
   level semantics remained SRE-specific (chaos engineering, MTTR, deploy
   frequency, on-call satisfaction).
2. **Scale convention drift** — the repo used zero-based `L0..L4` while the
   canonical bands are one-based (`level-1-emergent`..`level-5-self-optimising`),
   making "L2" ambiguous (Systematic as a scale level, Structured as a band
   index). dea-metamodel #214 proposes `L-0 Not Assessed + L-1..L-5` with
   capability ordinals aligned 1:1 to band ordinals; Autonomous Operations
   has adopted it; the gateway engine fix renders it.
3. **No current/future distinction** — the model measured only present-state
   practice; there was no concept of future operational readiness, and no
   separation of maturity from readiness from performance
   (CR-Model-Assessment-Operations-0001 §9C).
4. **Coverage gaps against the domain foundation** — no Operating Model
   dimension distinct from capabilities; service and process management
   conflated; no Resources & Assets; no explicit Governance & Resilience
   home for risk/continuity/controls; no Enterprise Value Realization
   distinction from efficiency.
5. **Owner cleanup deferred** — the stable register still named
   `operations-v2-draft.yaml`; `standard.yaml` pinned model version `1.0.0`;
   the worked example predated the register; `local_validate.py` validated
   only the v1-era artifacts.

## §2 Objectives

- Restate the model as the **parent operational assessment** for enterprise
  operations, per the domain foundation (CR-Operations-00000) — comprehensive
  coverage, dual present/future perspectives, explicit value realization,
  specialized depth delegated to sibling models via touchpoints.
- Adopt the `L-0 + L-1..L-5` scale convention (band-aligned ordinals,
  band-edge points), annotated adoption-pending #214.
- Encode CR-Model-Assessment-Operations-0001's criterion attribute table
  (question/intent via statement+intent, current & future expectations,
  evidence, indicators) on every criterion.
- Preserve ecosystem invariants: contract handshake, canonical bands bound
  (never restated), criterion-ID permanence via published migration maps,
  three CI levels, repository standard conformance.

**Non-goals:** becoming an autonomous-operations model (D07/D08 assess
governed, integrated autonomous execution; depth remains with the AO peer);
new scoring bands (canonical v2 bands retained); redefining the metamodel;
averaging specialized-model scores into the Operations Index.

## §3 Reconnaissance → decisions (retain / revise / introduce / retire)

| Decision | Items |
|---|---|
| **Retain** | contract handshake; `dea:maturity-bands-v2@v1.0.0` binding; band widths/multipliers; evidence confidence levels; touchpoint mechanism and all six peer records; `operations-modernization` component reuse; benchmarking/campaign mechanics; criterion-ID permanence rule |
| **Revise** | scale → `dea:scale-operations-v2` (L-0..L-5, enterprise-operations level semantics); register → v3 taxonomy with dual-perspective fields; evaluation → band-edge points, `level_band_map`, perspectives, four result views; questionnaire → 132 dual-perspective entries (generated); evidence schema → v3 id pattern, four derived views; blueprint deduction → remapped keys + resilience/value/gap rules; README (full rewrite); `standard.yaml`/manifest/model.yaml coherence; worked example + campaign recomputation; validator scope |
| **Introduce** | nine-dimension taxonomy D01..D09 (44 sub-dimensions, 132 criteria); `perspectives` (current-realization / future-readiness) with per-criterion `current_expectation` / `future_expectation`; readiness index + transformation gap; `ops_stage_by_ordinal` additive vocabulary; `migrations/v2-to-v3-map.yaml`; `docs/domain/enterprise-operations.md`; this CR |
| **Retire** | `maturity/model/operations.yaml` v1 identity register (superseded by the v3 register at the same path — also fixes the gateway loader path); `operations-v2-draft.yaml` filename (owner cleanup recorded in 2.0.0 CHANGELOG); `(level/4)*100` point formula; v2 dimension names in the manifest; README's stale status/layout/provenance sections |

## §4 Target architecture

**Dimensions** (weights sum 1.00): D01 Operating Model 0.12 · D02 Operational
Capabilities 0.12 · D03 Value Streams & Processes 0.12 · D04 Service &
Delivery Management 0.11 · D05 People & Organization 0.10 · D06 Resources &
Assets 0.09 · D07 Information & Technology 0.12 · D08 Operational Governance
& Resilience 0.11 · D09 Operational Performance & Value 0.11.

**Perspectives** — every criterion carries both, scored on the same scale,
weights and points:

| Perspective | Field | Aggregates to |
|---|---|---|
| Current Operational Realization | `current_expectation` | Operations Index → band → effort-adjusted value |
| Future Operational Readiness | `future_expectation` | Readiness Index → Transformation Gap (readiness − current) |

**Value distinction** — D09 keeps *Operational Efficiency & Effectiveness*
(SD02) and *Enterprise Value Realization* (SD03) as separately scored
sub-dimensions; the performance-and-value view reads them apart (an
enterprise can be efficient and strategically misaligned, and the model must
expose both).

**Specialization boundary** — this model assesses whether specialized
execution (notably autonomous execution) is governed, integrated and aligned;
the AO peer assesses the depth of the mechanisms. No cross-model averaging
(`touchpoints.yaml` v0.3.0 header rule).

## §5 Scale decision

Adopt `L-0 Not Assessed + L-1..L-5` per dea-metamodel #214: capability
ordinals align 1:1 with canonical band ordinals; criterion points become the
band's upper edge (20/45/70/88/100); L-0 is strictly "not assessed" —
evidenced absence scores L-1. Level *names* remain the canonical band
vocabulary (Emergent..Self-Optimising) shifted by one; the enterprise-
operations progression vocabulary (Absent, Initial, Defined & Managed,
Integrated, Adaptive) rides as additive metadata (`ops_stage_by_ordinal`).
Level *semantics* are rewritten to enterprise operations. Rationale: the
alternative (staying zero-based) would leave the known ambiguity in place and
force a second breaking wave after #214 ratifies; the gateway engine fix
(`fix/level-convention-agnostic`) already renders six-level ladders.

**Gate:** the scale annotation and CHANGELOG mark the renumbering
*adoption pending dea-metamodel #214*. Release sequencing (tagging v3.0.0,
registry registration) waits for the coordinated wave decision, mirroring the
AO precedent.

## §5a Post-2.1.1 reconciliation (recon 2026-11-23, main 3518070 → 57f33d6)

While this programme was in flight, main released 2.1.0/2.1.1 with two
approved change requests that partially intersect this CR. The v3 branch is
rebased onto 2.1.1 and reconciled as follows:

| Main decision (approved) | v3 reconciliation |
|---|---|
| **CR-AM-17** — identity-only scale migration (`L-0` sentinel + `L-1..L-5`, `dea:scale-operations-v2` v2.0.0; `migrations/scale-v1-to-v2-map.yaml` crosswalk; legacy L0 → L-1, never L-0) | Adopted wholesale: ids, sentinel semantics, crosswalk and **criterion score preservation (0/25/50/75/100)** are kept unchanged; the branch's earlier band-edge point scheme (20/45/70/88/100) is withdrawn. The register carries `unassessed_level: L-0` and a `scale_reference` at the release version. |
| **CR-AM-19** — marginal-band EAV, `EAV(S) = Σ(Pk(S)/Mk)`, max 53.1666666667 | Adopted wholesale: evaluation steps, worked example and campaign recomputed (63.7 → 44.15; campaign 41.95 → 45.55, Δ 3.60); the branch's whole-score-times-multiplier values are withdrawn. |
| **CR-AM-17's preserve-verbatim level semantics** (SRE-flavored characteristics kept at 2.1.0) | **Superseded for v3 by deliberate decision** (confirmed against the attached CR-Operations-00000 / CR-Model-Assessment-Operations-0001 foundations): this MAJOR release evolves level definitions/characteristics to enterprise operations (§5 above). Identifiers, names, bands and score preservation are untouched; the evolution is confined to definition text and is traceable to this section. |
| **2.1.1 reciprocal touchpoints v0.2.3** (`peer_touchpoint_id`/`mirrors`/`reciprocity: mirrors-tp-*`; AO root-cause correction to `OPS-D5-SD2-C05`) | Preserved in touchpoints v0.3.0; the corrected mapping now points at the v3 problem-management criterion (`OPS-D08-SD05-C03`); all `ours:` ids remapped; peer statuses → `peer-remap-pending`. |
| **2.1.0 evidence schema `criterion_score`** (`level_id`/`assessment_status`/`score`/`evidence_confidence`, L-0 and legacy-L0 rules) | Preserved verbatim; v3 composes it per perspective (`current` + `future`) and extends the criterion pattern to the v3 taxonomy. |
| **2.1.0 reader-first README** (personas, mermaid, scoring walkthrough) | Kept as the skeleton; content updated to nine dimensions, the perspectives, enterprise-operations level semantics and 3.0.0 status. |
| **2.1.x keeps both register files live** (identity register at `operations.yaml` + `operations-v2-draft.yaml`) | Not carried forward: v3 consolidates into a single register at `maturity/model/operations.yaml` (the gateway loader resolves this path first); the 2.1.x additions to both files are folded in. |
| **2.1.x validator rewrite** (scale/sentinel/crosswalk/EAV-boundary checks, VERSION handshake) | Kept as the base; v3 adds register taxonomy, dual-perspective fields, questionnaire/evidence/touchpoint/migration resolution and full version coherence on top. |

Net scoring contract after reconciliation: criterion scores preserved at
0/25/50/75/100 (CR-AM-17), aggregation unchanged, marginal-band EAV
(CR-AM-19), dual perspectives and transformation gap additive (CR-OM-01).
Historical indexes re-aggregate only through the v3 dimension/criterion
re-homing and weights — never through point changes.

## §6 Implemented phases

| Phase | Content | Exit criterion (met) |
|---|---|---|
| 0 | Reconnaissance & blueprint (this CR §§1-5) | decisions table approved in-repo |
| 1 | `maturity/scale.yaml` v2 | 6 levels; L-0 named Not Assessed; enterprise-operations semantics; validator enforces |
| 2 | v3 register at `maturity/model/operations.yaml` (removes `-draft` filename) | 9 dims / 44 SDs / 132 criteria; dual-perspective fields on every criterion; weights 1.00; 51/51 v2 lineage |
| 3 | evaluation + questionnaire + evidence schema + blueprint deduction | band-edge points; `level_band_map` binding; questionnaire ids ≡ register ids; evidence pattern accepts all ids; four result views |
| 4 | touchpoints v0.3.0 | all `ours:` ids remapped; specialization rule recorded; peer statuses `peer-remap-pending` |
| 5 | migrations v2→v3; campaign + example recomputation; metadata coherence (model.yaml/VERSION/standard.yaml/manifest); validator v3; README rewrite; CHANGELOG | Level 1 validator green end-to-end |

## §7 Ecosystem dependencies and follow-ups (out of repo scope)

1. **dea-metamodel #214 ratification** — gates release tagging/registry
   update; scale annotated pending.
2. **Peer reciprocity wave** — AO, services-delivery, technology, DT and DTO
   mirror records still cite v2 `OPS-D*` ids; each peer needs the v3 remap
   (map provided by `migrations/v2-to-v3-map.yaml`).
3. **Gateway deployment** — merge/deploy `fix/level-convention-agnostic` so
   the six-level ladder renders correctly; then re-index the model.
4. **assessment-registry record** — version/scale/dimensions update at the
   release boundary (post-ratification), plus v3.0.0 tag per CONTRIBUTING.
5. **dea-assessment-operations** instrument repo — same scope refresh against
   this domain definition (separate CR).
6. **maturity-touchpoint-contract** (#213) — publish; then this repo's
   touchpoints.yaml can leave `status: draft`.

## §8 Risks

| Risk | Mitigation |
|---|---|
| #214 not ratified (or changed) | renumbering is isolated to `level_map`/`points_map` + scale/register/q-e annotations; a reverted convention is a contained change |
| Benchmark discontinuity for 2.x records | `migrations/v2-to-v3-map.yaml` re-projects criteria, levels and points; band scheme unchanged so resolved bands remain comparable |
| Weight rebalance shifts historical indexes | weights are part of the migration note; campaigns must be re-baselined under v3 weights (worked campaign demonstrates) |
| Peer reciprocity CI warnings | `peer-remap-pending` statuses declared; soft-fail window per CR-AM-13 §5 |
| Register size (132 criteria) raising assessment effort | questionnaire is generated; L-0 Not Assessed allows partial assessment without inflating the index; campaigns can scope by dimension |
