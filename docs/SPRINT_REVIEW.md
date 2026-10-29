# Research alignment and sprint reviews

Established 2026-10-30 at the researcher's request. This is the sprint-boundary
check, not an additional application, dashboard or scheduled automation.

**Approved baseline**

The initial service idea was narrowed, with the researcher's approval, to a
reproducible model study. Match **different denim products by their photographed
appearance**; preserve observed lighting and wear, and distinguish silhouette
from surface/wash. Personal taste, original-fabric reconstruction and mobile UI
are outside this scope. The current primary ambition is better matching quality
than a specified strong general multimodal comparator on a defined denim task.
Efficiency can be reported separately and does not replace that ambition.

This baseline follows the recorded [scope history](RESEARCH.md),
[axis correction](AXIS_SEPARATION_AUDIT.md) and the researcher's latest approval
of the [regional/attribute learning proposal](LITERATURE_REVIEW_20261030.md).
The original attached roadmap is not present at its previously supplied local
path; it has not been reread or claimed recovered. Do not invent its detailed
milestones. Later approved decisions take precedence over the original app idea.

Approved flow: permitted data/provenance -> readable garment and regional inputs
-> product/duplicate/capture groups and splits -> reliable axis-specific
supervision -> controlled adaptation -> independent, matched comparison -> failure
analysis/literature investigation -> the next justified iteration.

**Boundary checklist**

| Review item | Record, with evidence |
|---|---|
| Planned versus actual | Which flow step moved? What is unfinished or a detour? |
| Research evidence | Separate runnable code, fitting, development and new-group quality; link measurements |
| Known limits and feedback | Include unresolved failures and external feedback; classify resolved, tested but unresolved, deferred or not investigated |
| Follow-up investigations | For each material limit: question, next check/source, expected artifact, decision affected and priority |
| Human cost and resources | New useful independent constraints, actual human workload and measured compute; unavailable timing stays unknown |
| Next step | One main hypothesis and deliverable; proceed/repair/hold decision; exact human/access gate |

Keep each review compact. Reuse existing evidence rather than duplicating logs.
When a new paper or error suggests a direction change, explain the implication
and obtain direction confirmation; do not start a new architecture by default.
Code tests and document checks do not constitute matching-performance evidence.

Copy this short record at every sprint boundary:

```text
Date / sprint / approved target:
Planned flow step -> actual step, evidence:
Matching-quality delta / uncertainty:
Unresolved limits, deviations and feedback:
Next investigations (priority -> question -> check/artifact -> decision):
Human work / measured compute / unavailable measurements:
Decision and next deliverable / human gate:
```

**Review 001 — 2026-10-30: calibration and literature phase**

- Target/actual: prepare task-aligned supervision for denim adaptation. Attribute
  feasibility and paper analysis completed; regional axis-specific learning has
  not started. Repeated coarse-tag prompting was a detour from matching quality.
- Evidence: latest eight-photo teacher agreement was 7/8 family,5/8 lightness
  (2B),5/8 and6/8 (4B); all96 drafts remain excluded. These are annotation findings,
  not retrieval gains. [Audit](ATTRIBUTE_AUDIT.md). The last new-query human
  continuation score declined 0.3841 ->0.3513 in a three-query development check.
  No independent quality improvement or general-model superiority established.
- Limits/feedback: attribute/local objectives unimplemented; useful candidate
  coverage and readable detail unestablished; strong-model comparison absent;
  independent raters/final test and artifact-release rights unresolved. Earlier
  infrastructure/evaluator issues improved, but requests for real quality evidence
  remain open. Original roadmap file unavailable; use the approved scope history.
- Priority1 investigation: audit existing photo resolution, visibility and plausible
  cross-product alternatives; produce a private development manifest/visual check
  before requesting labels. This decides whether current data supports the trial.
- Priority2 investigation: compare garment-wide versus hip/thigh evidence, separately
  for silhouette and surface; prepare a minimal controlled adaptation using the
  current backbone. This tests regional information rather than another tagger.
- Priority3 investigation: define a strong general-model comparison with the same
  evidence/pools and human truth; establish actual model access/provenance before
  scoring. Prepare inputs first; do not spend on an API without authorization.
- Human/resources:17 attribute photos judged across three rounds; no hours ledger.
  The literature phase created no training or compute result. Existing70 tests are
  software evidence only. Raw responses and remote runtime summaries stay private.
- Decision: researcher approved the quality-first regional/axis-specific experiment
  and mandatory sprint review. Begin data-readiness work; next human gate is a small
  scoped comparison after plausible candidates exist, or a concrete access choice.
  Continue independently through preparation; no additional confirmation of the
  already approved research direction is needed.

**Active sprint checkpoint — regional data preparation**

Source verification:96/96 existing photos hash-valid, all228x298. Eight observations,
16 garment/hip-thigh rectangles and three blind boards are prepared; human labels0,
training eligible0, quality improvement unmeasured. [Readiness evidence](verification/regional_readiness_20261030.json).
Next intervention is six scoped human preferences. The main limitation is small
source resolution and unverified close-match availability. If answers mostly reject
both alternatives, investigate better cross-product candidate supply before training;
if scope is unreadable, improve input detail/regions. Do not compensate by inventing
positives or generating more triplet combinations. This checkpoint does not mark the
adaptation experiment complete; the sprint review must be revisited at its boundary.
