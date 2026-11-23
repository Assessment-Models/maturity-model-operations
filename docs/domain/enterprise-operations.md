# Enterprise Operations — domain definition and assessment method

The authoritative domain foundation for the Operations Maturity Model
(`dea:maturity-operations`). Distilled from CR-Operations-00000
("Understanding and Assessing Enterprise Operations") and
CR-Model-Assessment-Operations-0001 (model evolution architecture); the
normative encoding of this document is the v3 criteria register
(`maturity/model/operations.yaml`) and scale (`maturity/scale.yaml`).

## 1. Definition

**Operations**, in an enterprise context, is the organized realization of an
enterprise's purpose through the coordinated execution of its activities,
processes, resources, capabilities and decisions to produce intended outcomes
and deliver value.

It is the dimension of the enterprise concerned with how the organization
actually works: how it transforms intent into action, how it produces and
delivers its products and services, how it serves customers and stakeholders,
and how it sustains and improves the systems through which value is realized.

Operations is **not** synonymous with processes, nor with the day-to-day
running of a business, nor with IT operations. Processes are among the
*mechanisms* through which operations are realized. Operations is the broader
organizational construct encompassing the structures, capabilities, people,
resources, technologies, controls and execution mechanisms that make the
enterprise work.

The relationship the assessment rests on:

```
Purpose & strategic intent   →  why the enterprise exists and what it intends
        ↓
Enterprise operations        →  how the enterprise organizes and executes:
                                  capabilities, processes, people &
                                  organization, resources & assets, information
                                  & technology, governance & controls
        ↓
Operational execution        →  activities, decisions, interactions,
                                  transactions, service delivery
        ↓
Outcomes & value realization →  customer value, business performance,
                                  stakeholder outcomes, sustainability
```

Operations is therefore not merely an execution layer; it is the
organizational system through which the enterprise realizes its purpose.

## 2. The nine assessment dimensions

| Dim | Dimension | What it examines |
|---|---|---|
| D01 | Operating Model | How the enterprise structures, organizes and coordinates its operations |
| D02 | Operational Capabilities | What the enterprise must be able to do to execute its business |
| D03 | Value Streams & Processes | How work is structured, coordinated and executed to produce outcomes |
| D04 | Service & Delivery Management | How operational services and products are fulfilled and delivered |
| D05 | People & Organization | How roles, responsibilities, skills and structures support execution |
| D06 | Resources & Assets | How physical, financial, human and other resources are mobilized and managed |
| D07 | Information & Technology | How information, data, applications and infrastructure enable operations |
| D08 | Operational Governance & Resilience | How decisions, policies, controls, risks and accountability are managed |
| D09 | Operational Performance & Value | How performance is measured and how activity realizes enterprise value |

The dimensions are interdependent — an enterprise may have well-defined
processes but insufficient capabilities, capable people but fragmented
information systems, sophisticated technology but ineffective governance. The
assessment therefore examines both individual dimensions and their collective
effectiveness.

Structural decisions embedded in the taxonomy (CR-Model-Assessment-Operations-0001 §3):

- **Operating Model is distinct from Operational Capabilities** — a
  well-designed operating model can lack the capabilities to realize it, and
  vice versa.
- **Value Streams & Processes are distinct from Service & Delivery
  Management** — processes describe how work is performed; services and
  delivery concern what is provided and how commitments are fulfilled.
- **Information & Technology is deliberately broad** — technology operations
  are not reduced to infrastructure management or SRE.
- **Operational Performance & Value is an explicit dimension** — the
  relationship between operations, business outcomes and value realization is
  a first-class assessment concern, with *efficiency/effectiveness* and
  *enterprise value realization* as separately readable sub-dimensions.
- **Governance and Resilience are combined** — risk, compliance, continuity
  and controls collectively establish the conditions under which the
  enterprise can operate reliably and responsibly.

## 3. The six assessment lenses

Within every dimension, the assessment distinguishes whether an operation
merely *exists*, whether it *works*, and whether it can *evolve*:

| Lens | Central question |
|---|---|
| Definition | Is the operational construct clearly defined, understood and documented? |
| Capability | Does the enterprise possess the ability to perform the required work? |
| Execution | Is the work consistently and effectively performed? |
| Integration | Are the operational components coordinated across organizational boundaries? |
| Control | Is execution governed, monitored, assured and managed within acceptable risk parameters? |
| Adaptability | Can operations respond to change, learn and improve without disproportionate disruption? |

The lens vocabulary also informs the register's `indicators` categories
(efficiency, effectiveness, quality, responsiveness, reliability, resilience,
compliance, agility, innovation, value realization).

## 4. The maturity progression

The scale binds the canonical v2 bands (non-linear widths 20/25/25/18/12,
effort multipliers 1.0 → 6.0). Under the `L-0 + L-1..L-5` numbering
(dea-metamodel #214; adoption pending ratification):

| Level | Name | Band | Enterprise-operations stage |
|---|---|---|---|
| L-0 | Not Assessed | — (0 pts) | criterion not assessed; never inflates the index |
| L-1 | Emergent | 1 · Emergent | Absent — largely dependent on individual effort |
| L-2 | Structured | 2 · Structured | Initial — repeatable through established practice |
| L-3 | Systematic | 3 · Systematic | Defined & Managed — measurable and manageable |
| L-4 | Adaptive | 4 · Adaptive | Integrated — enterprise-integrated, performance-driven |
| L-5 | Self-Optimising | 5 · Self-Optimising | Adaptive — learns, anticipates, increasingly autonomous execution |

Two cautions, normative for this model:

1. **L-5 does not require autonomous operations.** An enterprise can sustain
   the highest level with substantial human decision-making. Autonomous
   execution is a *specialized* maturity (Autonomous Operations Maturity
   Model), not a prerequisite of the general level.
2. **Maturity is not performance.** Highly mature governance can coexist with
   poor results, and excellent results can occur despite weak
   institutionalization. The model therefore measures maturity (how
   institutionalized the mechanisms are), performance (what results they
   achieve — D09) and readiness (how prepared the enterprise is for future
   requirements) as distinct views.

## 5. Three-layer assessment architecture

The model separates what is assessed from how and what it establishes:

1. **Operational scope** — the nine dimensions (what is being assessed).
2. **Assessment criteria** — the dual perspectives (current realization /
   future readiness), lenses and evidence requirements (how each element is
   evaluated).
3. **Assessment results** — maturity, effectiveness, capability gaps,
   performance gaps, risks, improvement opportunities, modernization
   priorities (what the assessment establishes).

This separation prevents dimensions being confused with criteria or outcomes:
*Operational Capabilities* is a dimension being assessed; *capability* is also
an assessment lens; neither is an assessment result.

## 6. Evidence and triangulation

Assessments draw on multiple evidence sources rather than management opinion
alone: operating model documentation and organizational structures; capability
maps; process architectures and workflow records; policies, standards and
control frameworks; SLAs and performance dashboards; resource utilization and
financial records; application, data and technology architecture; risk
registers, audit findings and incident records; interviews with operational
leaders, process owners and frontline personnel; direct observation.

Triangulation is essential: **a documented process does not necessarily
represent the process being performed in practice.** The evidence schema
(`maturity/evidence/schema.yaml`) encodes confidence levels accordingly
(observed 1.0 → unverified 0.3).

## 7. Distinctions the assessment must respect

| Concept | Primary concern | Relationship to operations |
|---|---|---|
| Strategy | Where and why the enterprise competes | Establishes operational direction and priorities |
| Business Model | How the enterprise creates, delivers and captures value | Defines what operations must support |
| Operating Model | How the enterprise organizes itself to execute | The structural arrangement for operations |
| Business Architecture | How business elements relate and work together | Structural and semantic understanding of the business |
| Enterprise Operations | How the enterprise executes and realizes its purpose | The actual organizational system of execution |
| Technology Architecture | How technology components are structured | Technological foundations for execution |
| Enterprise Performance | How well the enterprise achieves objectives | Measures the results of operational and strategic execution |

Especially: the **operating model describes design; operations describes
actuality** — including how effectively the design is realized. And
**technology is an enabler, not the domain**: operations also encompasses
organizational, human, physical, informational and governance mechanisms.

## 8. Foundational constructs

The register operationalizes these constructs:

| Construct | Purpose | Where it lives |
|---|---|---|
| Operational Domain | The scope of enterprise operations | `domain: operations` + this document |
| Operational Capability | What the enterprise must be able to do | D02 |
| Operational Process | How work is performed to achieve outcomes | D03 |
| Operational Service | What is provided to a consumer | D04 |
| Operational Resource | What is mobilized to support execution | D06 |
| Operational Control | How execution is constrained and assured | D08 |
| Operational Performance | How execution and outcomes are measured | D09 |
| Operational Maturity | Degree of institutionalization | scale + Operations Index |
| Operational Resilience | Ability to sustain and recover under disruption | D08-SD04/SD05 |
| Operational Intelligence | Ability to understand, anticipate, improve | D09-SD04 |

The constructs are related through the register's semantic structure rather
than treated as independent assessment categories.

## 9. The three questions that shaped this model

1. **Scope** — assess both how well the enterprise operates *today* and
   whether it possesses the operational capabilities its *future strategy*
   requires, as distinguishable perspectives integrated in one model
   (→ dual perspectives).
2. **Maturity** — operational maturity primarily measures the enterprise's
   ability to coordinate, adapt and autonomously execute over time, with
   institutionalization as the prerequisite, not the summit
   (→ L-4 Adaptive / L-5 Self-Optimising semantics).
3. **Value** — the assessment establishes whether the enterprise can
   consistently realize the value promised by its business model, not merely
   whether it operates efficiently (→ D09-SD03 Enterprise Value Realization).

**Central proposition:** enterprise operations should be assessed not simply
by how efficiently an organization performs its existing activities, but by
how effectively, reliably and adaptively it can mobilize its capabilities to
realize enterprise outcomes. That is what makes an operations assessment
strategically relevant rather than merely an operational audit — and it
creates the natural foundation for an operations modernization assessment:
identifying not only what is inefficient today, but what must fundamentally
change in the enterprise's ability to operate tomorrow.
