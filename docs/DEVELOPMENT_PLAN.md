# Denim Atlas development plan

Updated 2026-11-05 after Sprint 2. This replaces the earlier forward plan;
completed experiment records and their frozen results remain unchanged.

## Research objective and task

Learn photographed denim resemblance across different products and test whether
adaptation improves matching over the frozen encoder and a specified strong general
multimodal comparator. Quality is the primary goal; efficiency alone is insufficient.

Keep two inspectable axes:

- **Silhouette:** visible volume and upper-leg/knee/hem profile.
- **Surface:** photographed color family, lightness, apparent cast, fade contrast,
  pattern/location and distressing. Preserve observed lighting and wear.

The [working definition](SIMILARITY_DESIGN.md) exists, but perceptual tolerances and
reliable evaluation truth are not yet established. Retail cut names, shared product
identity, teacher agreement and training loss are not substitutes. Overall similarity
must not hide a large mismatch on one axis; the acceptance rule still needs calibration.

## Completed work and actual evidence

| Sprint | Delivered | Scientific conclusion |
|---|---|---|
| 1 — input execution recorded; research gate pending | Cached-source audit; 27 observations, 54 regions; train 18/development 9; 20 machine decisions yielding 13 train and 6 development constraints, with 1 neither excluded | Ready for a small weak-supervision pilot. No independent ground truth or quality gain established |
| 2 — pipeline check recorded; research gate pending | Frozen FashionSigLIP, garment/regional controls and two 64-D projections; one fixed 200-step run on T4; checkpoint restoration and error analysis | Development agreement remains 2/3 per axis for E0/E1/E2. No net gain; silhouette fixes one preference and regresses another |

[Input contract](SPRINT1_INPUT_CONTRACT.md) · [Sprint 2 experiment](REGIONAL_AXIS_PILOT.md) ·
[Frozen result record](verification/sprint2_results_20261105.json).

All 1,200 cached source images are 228x298, including 562 provisionally accepted
observations. The current three development anchors contain no wearing photos and
no case with different preferred candidates between the axes. The 147,456 head
parameters are underdetermined by 13 dependent training constraints. All 96 rejected
Qwen attribute drafts remain excluded. These limits are not resolved by the latest run.

## Revised sequence from the current checkpoint

### Sprint 3 — data feasibility first, then independent evaluation and comparator

First establish whether permitted high-resolution wearing originals contain readable
hip/thigh washing detail and sufficient independent garment coverage. Report actual
original downloads, native garment-region detail and remaining supply gaps before
advancing. Keep the detailed-wash objective; the researcher declined automatic
scope reduction. Until data and human truth gates pass, this stage remains pending.

1. Specify the exact available strong general model, version, execution route,
   image preprocessing and expected access/cost. Prepare the fixed input/prompt
   bundle before any request for paid API authorization. Current conversational
   labels have no exposed checkpoint and are not a named GPT API benchmark.
2. Freeze the comparison question and endpoint for each axis. Specify how useful
   matches, ties, neither and unknown are handled. Relative A/B labels support
   preference agreement; graded nDCG requires separately justified relevance grades.
3. Assemble readable, permitted evaluation material with known source/duplicate
   groups separated from training. Include wearing views, axis-conflicting choices,
   plausible close alternatives and difficult negatives. Keep prior selected/model-
   inspected material marked as development; do not rename it an untouched final test.
4. Use roughly 30 varied development anchors as an initial coverage target, not a
   promise of statistical adequacy. Define the candidate count, views and complete
   annotation workload before scaling. If appropriate alternatives or readable
   detail are missing, repair those inputs rather than manufacturing positives.
5. Freeze human evaluation judgments before inspecting rankings. Machine labels
   are allowed for training and engineering diagnostics only, not development/final
   quality truth. The researcher approved an estimated30–40-minute independent
   evaluation session, not manual training annotation. Training annotation remains
   delegated to the visual assistant. Record evaluator identity/version and whether
   evidence is human or machine. A teacher must not certify its own superiority:
   if reference judgments depend on the comparator itself, report agreement with
   that teacher, not independent quality.
6. Run the frozen encoder and strong comparator on the same evidence and pools.
   Report per-axis outcomes, coverage, ambiguity and failures. Within-pool ranking
   and full-gallery candidate retrieval are different endpoints.

**Exit:** a concrete, reproducible comparison can distinguish the proposed methods
on the intended task. If access or independent evaluation truth is unavailable,
report the exact gate; do not call an AI-agreement benchmark independent human truth.
No additional adaptation run is scheduled before these inputs are usable.

### Sprint 4 — one controlled improvement

Choose one intervention from the frozen comparison's failures. Candidates include
lower head capacity, better region alignment, more useful training relationships or
higher-detail source material. Keep unchanged controls and run the same evaluation
protocol. Do not change data, labels, capacity and aggregation simultaneously.

Start with the pinned FashionSigLIP encoder. A lower-capacity control can reuse
cached features. Unfreeze the last vision block only when the evidence implicates
missing visual representation rather than inadequate labels, coverage or capacity.
Compare a promising recipe across seeds before retaining it. After two no-gain
iterations on one hypothesis, summarize the failure and revise that hypothesis;
do not turn the stage into an unconstrained parameter sweep.

**Exit:** a measured development gain with paired cases and remaining regressions,
or a negative/inconclusive finding with the next evidence-driven decision.
Training fitting alone does not pass.

### Sprint 5 — independent comparison and research release

Freeze the selected recipe, checkpoints, comparator version, prompt and primary
endpoint before final evaluation. Use fresh protected groups and report silhouette,
surface, directly assessed overall acceptability where available, and relevant
view/detail slices. Report paired uncertainty at the anchor/group level, including
unknowns and neither outcomes. Do not choose a favorable threshold after seeing
final results or present a selected hard-case win as overall superiority.

An AI-judged result supports an AI-judged claim. A broad human-quality claim needs
independent human evidence; do not silently reintroduce a large manual training
assignment to obtain it. If that evidence cannot be obtained, narrow the conclusion,
not the recorded failure. Any change to the research goal needs a direction decision.

**Exit:** a reproducible win, loss or inconclusive result on the declared domain,
with limitations and rights-cleared code/results. No superiority claim without
matched evidence. Raw images, judgments, correspondence and model artifacts remain
private unless their separate release rights are established.

## Execution ownership and scope

Codex handles source preparation, crops, known-group protection, machine annotation,
experiments and error analysis. Human intervention is reserved for actual access,
cost/terms decisions or a research-direction choice; training annotation has been
delegated. Color/brightness-only work may be a diagnostic, but does not replace the
two-axis denim objective without approval. Mobile UI and shopping integration remain
outside this research scope.

Use the existing [sprint review](SPRINT_REVIEW.md) and [state](../PROJECT_STATE.md)
for brief result/limit/next-decision updates. Do not add another tracker or general
audit document by default. Tests establish software behavior, not matching quality.
