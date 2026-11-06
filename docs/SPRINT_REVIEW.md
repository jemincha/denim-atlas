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


2026-11-05: B/quality superiority and detailed washing retained; S1/S2 execution is recorded but research gates remain pending; the 3-anchor AI result cannot decide the quality hypothesis.
Human evaluation only (~30–40 minutes, estimate) is approved; machine labels stay training/engineering-only, never development/final quality truth; paid-model spending remains unapproved.
Source feasibility: 10 CC BY/CC0 wearing originals actually verified (up to3680x5520), with readable800x900 and2200x1600 detail crops; capture duplicates/occlusion remain, so30 independent usable anchors are not established.
Evidence: prior Commons source snapshots plus data/private/commons_wearing_20261105/source_images.csv (20 previews,6 new originals;4 originals reused from prior candidates); no new research document or JSON, no training or evaluation labels.
Next: expand readable independent source/candidate coverage, then freeze human rubric/endpoint/exclusions/stop rules and named comparator access before comparison; quality gate may close only after the independent evidence exists.

2026-11-05 annotation-scale follow-up: generated pairs do not multiply independent evidence; learning curves must report unique garment/capture groups and usable supervision, with fixed grouped splits and an untouched final human test.
Proposed teacher pilot: gpt-5.4-2026-03-05 (official dated image-input snapshot); reuse 17 coarse human judgments without supplying target answers, then inspect 10 available high-resolution originals; the previously inspected human set is development-only and cannot validate detailed washing or silhouette accuracy.
Extract observable axis-specific attributes with unknowns and spatial wash/fade information; equal attribute bins alone must not create positive pairs, and the teacher is not the final strong-general-model comparator.
Free-credit-only authorization received; API connection/balance and paid-fallback protection remain unverified: 27 initial calls plus at most10 retries, detail=high with at most2 images/request, verify total input<=7500 and cap output at4096 tokens (including reasoning), no tools; documented USD2.50/15 per1M input/output implies <=USD2.96703 token charges before tax, subject to preflight rate confirmation; no API key currently configured and no paid call made.
Access update: OpenAI Developers connected, but promo preview returned not_qualified (no new offer; existing free balance unknown); no key created or model called. User forbids execution without verified sufficient free credits and paid-fallback protection; keep the API pilot blocked until verified, with no top-up, paid fallback or research gate closure.

2026-11-05 fixed order: stop annotator search; saved-output errors -> frozen comparison bundle -> human evaluation -> current conversational assistant supervision only after human agreement -> independent garment/capture-group learning curves; no reordering or further training before the human gate.
Existing evidence:2B covers17 distinct human photos across heterogeneous runs;4B covers8. Matched8 agreement is family7/8->5/8 and lightness5/8->6/8;15 historical attribute/run errors classify as a/localization-confirmed0,b/observed anchor sensitivity2,c/incapacity-confirmed0,d/unresolved13;18 fenced-JSON transport failures are separate, with existing reparsed values, not18 visual errors.
Prepared private frozen bundle83d382802878564e44f088f86c4a142effd13abe166e45f5a227ebf56025501a:FashionSigLIP plus pinned CLIP/DINOv2,30 wearing queries/38 gallery images/90 pairs+9 delayed repeats/198 axis decisions in5-item batches;6 natural high-resolution queries,24 catalog228x298 queries and low-resolution gallery, so fine-wash and strong-general-model superiority remain unresolved.
Before labels: per-axis fixed-pool nDCG@3 only; unknown/conflicting repeats invalidate affected pools and all-zero pools have no nDCG; require>=20 complete pools and>=7/9 exact nonunknown repeats per axis or stop expansion/adaptation. Teacher coarse gate>=85% per human-labeled field plus>=2/3 nonblue items cannot approve unvalidated wash/shape attributes; all evaluation groups stay outside training.
Execution:86 local tests and JS syntax pass; crop checksums/30 known query groups/input archive validated, not certified product independence; no new labels/training/model/API run at bundle preparation. Kaggle authentication was subsequently restored as recorded below; GPU/right-tab visibility and the research gate remain pending.

2026-11-05 context handoff: official Kaggle SDK loopback OAuth completed; status api_verified and a separate CLI kernels-list read succeeded for jemincha. No more login or token entry is required.
Error decomposition and frozen input preparation are complete; no new GPU run, human judgments, teacher labels, training or paid API use. Next: private input upload -> frozen T4 comparison -> verified right-side human sheet,5 items at a time.
Bundle: runs/frozen_human_20261105 and data/private/frozen_human_20261105;68 crop hashes/ZIP CRC validated,30 queries/38 candidates/90 pairs+9 delayed repeats; only6 high-resolution queries, so detailed-wash evidence remains limited.
Resume from PROJECT_STATE.md in the same checkout; HEAD e1e4811 plus uncommitted comparison/state edits must be preserved. Local judge8882 responded200; actual tab visibility still requires verification, and exec PTY IDs must not be treated as visible Codex terminal sessions.
Approved order and human-only evaluation gates are unchanged. No forced context-compaction tool is available; this handoff records a restart point, not sprint/research completion or measured superiority over a general multimodal model.
2026-11-05 restart: independent human matching quality remains unmeasured; gate waiting, no sprint completion claimed.
User order supersedes handoff: visibly ready blind sheet (10–15 pairs/screen, autosave, repeats in a later session) -> frozen GPU features during judging -> approved three-line decision rules -> confirmed judgments/metrics -> inspected commit/push.
Gate1 blocked: right browser open returned queued only; UI inventory timed out and localhost8882 probe was denied socket access, so actual visibility is unverified; no alternative workflow pursued.
Existing sheet shows one pair at a time with five-item navigation batches and permits same-session repeats; requirements remain unmet, and random/hard selection provenance has not been verified on restart.
No authentication, annotator search, paid API, training, GPU launch, model ranking inspection, judgment creation, commit or push performed; resume at sheet readiness/visibility gate.
2026-11-06: gate waiting at step1, human matching quality unmeasured; evaluation UI now shows10 pairs/page, autosaves/restores and supports zoom without model scores/ranks; frozen packet/pools unchanged.
Selection provenance:30 preselected anchors x3 explicitly assigned candidates=90 pairs; only presentation order was randomized; no documented random-vs-hard strata, so no representative-sampling claim.
Delayed9 repeats require90 complete first-session pairs, explicit session finish,>=30 minutes and a new tab session; first-session grades stay locked thereafter; storage failures lock input.
Validation: synthetic JS checks cover ten cards, autosave/reload, time AND session gates and storage denial;15 related Python tests pass; real-browser layout/zoom/storage and actual right-tab visibility remain unverified (open queued; iab unavailable).
No new judgments, model ranking inspection, GPU/training/API/authentication, commit or push; no new research document/JSON. Next remains visible-sheet gate, then feature-only GPU during judging, approved decision rules, confirmed-label metrics and inspected push.
2026-11-06 human save: researcher reports completing/saving sheet; existing Downloads export validates against frozen packet/rater/rubric, with90 complete primary pairs on both axes and0/9 delayed repeats (9 missing trials/axis).
Gate waiting: delayed repeat session/export missing; no repeat-agreement or model metric calculated, scores/rankings unopened, no GPU/training/authentication/API/commit/push and no new research document/JSON.
Next human action: finish first session, wait>=30 minutes, close/reopen sheet in a new tab session, judge9 delayed pairs and save again; feature-only GPU and approved decision rules remain outstanding before interpretation, with strong-general-model superiority unmeasured.
2026-11-06 delayed completion: latest existing Downloads export validates against frozen packet, with90 primary+9 repeat pairs complete on both axes (198 decisions,0 missing); model scores/rankings and repeat agreement remain unopened/uncomputed.
GPU timing deviation: feature extraction was not started during judging. Existing authenticated Kaggle read succeeds; target frozen-input dataset absent;69-entry input ZIP CRC and embedded source compilation pass, with no ratings/secrets in upload payload.
Gate waiting: automatic approval review rejected private Kaggle photo/crop upload for missing explicit payload/destination authorization; no upload/GPU run, bypass, authentication repeat, paid API or training occurred.
Required permission: send inputs.zip (68 crops+manifest) to private jemincha/denim-atlas-frozen-human-inputs for pinned FashionSigLIP/CLIP/DINOv2 features only; approved three-line decision rules still precede interpretation, with independent model quality/general-VLM superiority unmeasured.
2026-11-06 explicit upload approval received: private frozen-human-inputs created, frozen-human-comparison v1 RUNNING on requested free T4 (3600s cap); features only, no labels/training/paid API, rankings/scores unopened; research gate waiting for decision-rule approval.
APPROVED analysis contract (user fixed before output interpretation): primary per-axis fixed-pool nDCG@3;>=20 complete eligible anchors/axis and>=7/9 exact nonunknown repeats/axis required; unknown/conflicting-repeat pools excluded, zero-gain pools unscored; strict human-preference concordance excludes human ties, model ties count0.5, random concordance0.5 and random nDCG exact pool-permutation mean;10000 paired anchor bootstrap samples,seed51105,95% percentile CI; resolution/view slices and denominators separate, repeat consistency reference only, missing wearing/catalog contrasts explicitly unmeasured.
APPROVED decision1—stop additional fine-tuning for this packet if the same frozen encoder attains nDCG@3>=0.90 on BOTH axes, each95%CI lower>=0.80 and each paired advantage over random95%CI lower>0; common eligibility gates required, no general-VLM superiority claim.
APPROVED decision2—consider slice-targeted adaptation only if decision1 fails, common gates pass, and a predeclared slice with>=5 anchors has nDCG@3 at least0.15 below its complement with anchor-bootstrap deficit95%CI lower>0; exploratory signal only, no training authorized; otherwise inconclusive.
APPROVED decision3—if either axis has<20 eligible anchors or<7/9 exact nonunknown repeats, limit performance claims to descriptive observable slices and pause adaptation; any reduction of the detailed-washing research goal requires separate human approval, never follows unreadable inputs alone; no automatic scope reduction or sprint closure.
2026-11-06 user fixed rules before interpretation; T4 v2 completed68 features/model(768/512/384), model/crop/uploaded-manifest hashes and preprocessing pass; v1 weight-hash variable collision repaired and identical extraction rerun, v1 excluded;89 Python tests+synthetic browser checks pass; no training/paid API.
Measured concordance95%CI, silhouette/surface:FashionSigLIP69.8[57.7,82.0]/67.5[53.7,81.5]%,CLIP62.3[47.2,76.4]/57.5[40.0,73.2]%,DINOv266.0[51.8,80.0]/65.0[46.2,81.8]%;random50%; exact repeats8/9 and3/9 (reference only), eligible complete pools29/24,nonzero28/21,strict preferences53/40;unknown trials0/5,conflicting pairs1/5.
Primary nDCG@3 silhouette/surface:FashionSigLIP.944[.908,.975]/.899[.830,.958],CLIP.901[.854,.943]/.853[.771,.927],DINOv2.908[.857,.953]/.857[.778,.932],random.873/.829;all between-model paired95%CIs include0;10000 anchor resamples,seed51105;human ties excluded from concordance/model ties0.5,unknown/conflicting-repeat pools excluded,zero-gain pools unscored.
Slices high/low original short side>=720/<720 confound natural/catalog wearing:complete pools6/23 silhouette,4/20 surface;concordance high/low FashionSigLIP83.3/68.1%,70.0/66.7%;CLIP16.7/68.1%,60.0/56.7%;DINOv250.0/68.1%,90.0/56.7%;pure catalog anchors0,all gallery228x298,so independent wearing/catalog contrast and detailed-wash/general-VLM superiority unmeasured;small-slice CIs descriptive.
Decision:rule3 applies(surface exact repeats3/9<7/9),descriptive claims only,adaptation paused,research gate waiting;no goal reduction/sprint closure. Next inspect existing repeat-disagreement evidence and rubric/detail limits before proposing further human work;raw ratings/photos/features/logs stay private;pre-push inspection passed15 selected text files,no photos/ratings/features/JSON/runs/auth scripts/binaries or secret-pattern findings.
