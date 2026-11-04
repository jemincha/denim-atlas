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

Historical October30 checkpoint; superseded by Review002 below.

Source verification:96/96 existing photos hash-valid, all228x298. Eight observations,
16 garment/hip-thigh rectangles and three blind boards are prepared; human labels0,
training eligible0, quality improvement unmeasured. [Readiness evidence](verification/regional_readiness_20261030.json).
Next intervention is six scoped human preferences. The main limitation is small
source resolution and unverified close-match availability. If answers mostly reject
both alternatives, investigate better cross-product candidate supply before training;
if scope is unreadable, improve input detail/regions. Do not compensate by inventing
positives or generating more triplet combinations. This checkpoint does not mark the
adaptation experiment complete; the sprint review must be revisited at its boundary.

**Review 002 — 2026-11-05: Sprint1 closure for a machine-supervised pilot**

- Target/actual: source -> regions -> grouped supervision -> training-input contract
  completed. The researcher explicitly delegated training judgments to the visual
  assistant; the pending manual gate was removed. This changes label provenance,
  not the quality-first, cross-product two-axis objective. [Inputs/contract](SPRINT1_INPUT_CONTRACT.md).
- Evidence: cached1,200 image hashes and562 reviewed hashes verified; all228x298,
  no URL fields in supplied metadata.27 observations/54 checked rectangles,
  train18/development9 with group/file/pixel guards.20 machine decisions produce
  18 strict preferences and1 distance tie;1 neither excluded. Human answers added0.
  [Frozen aggregate and hashes](verification/sprint1_machine_readiness_20261105.json).
- Quality delta: no new training or independent retrieval measurement this sprint.
  Machine development agreement will measure teacher reproduction. The teacher is
  this conversation's visual assistant, with no exposed exact checkpoint and no
  separate ChatGPT API call. No repeat-run consistency test, calibrated confidence
  or strong-general-model superiority is established. A15/B3/tie1/neither1 reflects
  this selected candidate set; no position-swap experiment was performed.
- Limits/feedback: usable training inputs now exist, but low source detail, mostly
  catalog views, dependent selected cases and tiny development coverage persist.
  A strict input gate is software evidence, not reliable ground-truth certification.
  The earlier70 tests and new validation checks do not resolve the demand for real
  quality results. Rejected96 Qwen drafts remain excluded; no broad teacher promotion.
- Priority1: run the planned E0/E1/E2 controlled adaptation on this frozen weak
  packet; save per-axis train/development margins and disagreement examples. This
  decides whether the regional/head implementation can learn transferable teacher
  constraints; a train-only gain triggers data/capacity diagnosis, not a quality claim.
- Priority2: inspect higher-detail permitted wearing sources before texture claims
  or scale-up; current metadata supplies no larger originals. The next source and
  readability audit determine whether fine wash matching is supportable.
- Priority3: fix accessible strong-comparator version and independent evaluation
  truth before final comparison. Randomized presentation and a second independent
  judgment route are required to investigate teacher/position bias. Do not request
  another manual training grid or invoke a paid API without new need/authorization.
- Human/resources:20 assistant-created decisions, no new human annotation burden
  and no paid API call. Private CPU audit version2 completed; wall time not measured.
  Legacy human overall judgments remain distinct from the new machine supervision.
- Decision: Sprint1 **complete for the amended small distillation pilot**, with
  limitations carried forward. Next is Sprint2's pinned-encoder regional/axis
  experiment; no new human intervention is required to begin that existing plan.

**Review 003 — 2026-11-05: Sprint2 regional/axis adaptation**

- Target/actual: prepared regions/grouped machine supervision -> frozen-feature
  E0/E1 controls -> two axis projections -> development comparison and error
  analysis completed. [Experiment](REGIONAL_AXIS_PILOT.md). No baseline-only detour,
  coarse-teacher prompting, UI construction or last-block unfreezing.
- Evidence:54 region features,147,456 head parameters,200 fixed steps; training
  strict agreement7/7 silhouette and5/5 surface plus a satisfied tie. Equal-axis
  loss0.066095->0.00006586; saved-head restoration and dev-gradient exclusion passed.
  Development remains2/3 per axis for E0/E1/E2; no net preference-agreement gain.
  Silhouette fixes1/regresses1; surface winners unchanged. [Results](verification/sprint2_results_20261105.json).
- Quality/uncertainty: these are machine-teacher development agreements across3
  selected anchors, not independent human matching quality or superiority to GPT.
  The previous new-query regression remains relevant; a training win does not
  supersede it. E2's untrained projection control and all outcomes are retained.
- Limits/feedback: fitting capacity is large relative to13 dependent constraints;
  development has0 axis-conflicting cases and0 wearing photos. This is an important
  coverage gap for the project's two-axis claim. Teacher checkpoint/repeat accuracy,
  fine source detail, independent comparison truth and release rights remain open.
  Requests for actual training/results are addressed; useful quality gain is unresolved.
- Priority1 investigation: freeze additional axis-conflicting and wearing
  development cases with reserved-group checks and machine labels before model
  outputs are examined; measure which axes actually disagree. This decides whether
  failure extends beyond the current catalog-heavy, shared-winner cases.
- Priority2 investigation: on the same cached features and labels compare reduced
  head capacity as one controlled change. Save train/development margins and paired
  outcomes; use this to decide whether more trainable scope is warranted. Do not
  change labels/data and capacity in one unexplained comparison or begin a sweep.
- Priority3 investigation: identify readable higher-resolution permitted wearing
  material and a versioned strong-model/independent-evaluation route. These decide
  support for fine wash claims and later superiority testing; no paid API assumed.
- Human/resources:0 new human decisions,0 paid API calls. Private TeslaT4 kernel
  version2 completed;46.71s encoding/training/save excludes setup/queue.84 local
  checks and CPU-recomputed E0/E1 outcomes verify software, not matching quality.
  Initial large-request400 and auto-extracted input-path failure were repaired
  without changing frozen data/config. Weights remain remote/private; no pending job.
- Decision: Sprint2 complete with **no demonstrated development-agreement gain**.
  Continue the existing controlled-improvement plan through data/coverage and
  capacity diagnosis; no new human training grid or broader backbone tuning.

**Feedback clarification — 2026-11-05, after Review003**

The external critique correctly identifies absent independent quality evidence,
proxy/fitting confusion and weak data/evaluation coverage. Its one-vector/no-axis-label
snapshot predates the completed two-head pilot and20 machine decisions; legacy joint
labels remain usable only for joint judgments, not axis decomposition. README also
retained contradictory historical preparation/no-training sentences; these are now
removed, and independent quality/no-gain evidence leads the page. No new audit
artifact or experiment was added. Before more adaptation, prioritize adequate
separate evaluation coverage and a specified general-model comparator. Training
judgments remain delegated to the visual assistant. Narrowing the task to color
alone or imposing manual training grids is not adopted without a direction decision.

**Review checkpoint — S2-2026-11-05 repository handoff**

The current README, state and revised development plan now describe the completed
Sprint 2 result and the same next sequence: Sprint 3 evaluation/comparator, Sprint 4
controlled improvement, Sprint 5 independent comparison/release. This replaces the
older four-sprint forward schedule; the two-axis quality objective is unchanged.
No new training, acquisition, labels or quality result was created by this handoff.
Machine-teacher limits, no-gain development outcome and missing independent quality
remain explicit. Existing result artifacts and implementation are preserved for
review at a fixed repository revision.
