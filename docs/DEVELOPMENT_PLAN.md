# Denim Atlas development plan — 2026-11-05

**Objective and current position**

Sprint2 execution is complete:54 frozen features, two axis heads and a matched
E0/E1/E2 development comparison. Agreement stays2/3 per axis; training fits all
strict constraints. [Results and diagnosis](REGIONAL_AXIS_PILOT.md). Proceed through
controlled coverage/capacity investigation, not broader backbone tuning.

November5 execution amendment: the researcher delegated the pending axis judgments
to the conversational multimodal assistant. [Sprint1 inputs](SPRINT1_INPUT_CONTRACT.md)
are now prepared:27 observations,54 regions,20 machine decisions and19 usable
constraints, with train18/development9 protected folds. The cached1,200 originals
are all228x298. Sprint1 closes for a **machine-supervised pilot**; it does not certify
teacher accuracy, independent matching quality or general-model superiority.
The manual gate described in the original plan below is superseded for this pilot.

Build a denim-adapted matching model that improves on a specified strong general
multimodal comparator for photographed, cross-product appearance. Report the task,
model/version, evaluation domain and uncertainty. Faster/cheaper inference is a
secondary benefit, not the primary success criterion. Match visible lighting and
wear; silhouette and surface appearance remain independently inspectable.

Working remote execution, adaptation, grouping and evaluation already exist.
562 catalog observations are provisionally accepted; their usefulness varies by
attribute. The full cached-source audit now covers1,200 images, not just96 previews.
The earlier three human boards remain unanswered and retired as a blocking gate;
their images may appear in the separately sourced machine packet. All96 rejected
Qwen attribute drafts remain outside training. Useful unseen matching improvement
and a direct strong-model comparison remain unestablished.

This operational plan follows the approved [literature-based direction](LITERATURE_REVIEW_20261030.md)
and [sprint review protocol](SPRINT_REVIEW.md). It does not reopen the app/UI scope.

**Four sprints, with an experiment at the center**

| Sprint | Deliverable and Codex work | Researcher intervention | Exit / repair decision |
|---|---|---|---|
| 1. Usable evidence and a fixed comparison contract | Completed source/crop audit, grouped machine-supervision inputs and comparison contract; preserve machine label provenance without fabricated human grades | Training annotation delegated to the conversational visual assistant on November5; no pending manual training gate | Ready for a small teacher-distillation pilot on broad visible cues. This amends the human-supervision assumption; teacher accuracy and final comparison access remain separate limits |
| 2. First regional/axis adaptation | Reuse FashionSigLIP on Kaggle. Cache garment-wide and hip/thigh features; train small silhouette/surface projections using only supported axis relationships. Run an unadapted reference, an untrained regional control and one adapted configuration. Save manifests, run summary and example failures | Check a small set of disagreements only if labels/regions are ambiguous | A real train->validation cycle with all outcomes reported. Training loss alone does not pass. If fit improves but validation does not, inspect data/labels and head capacity before unfreezing more weights |
| 3. Controlled improvement | Change the component implicated by Sprint2: candidate relationships, region alignment, image detail, aggregation or trainable scope. Unfreeze the last vision block only as a separate justified experiment. Compare a promising recipe across three seeds where compute permits | Confirm only informative comparisons or a material direction/resource change | Keep a change only with validation evidence. After two no-gain iterations on the same hypothesis, brief the failure and revise the hypothesis; do not silently run another parameter sweep |
| 4. Independent comparison and research release | Freeze recipe, checkpoints and comparator prompts; evaluate fresh group material, report axis/joint quality and failure slices; prepare reproducible commands, results and figures. Publish only permitted artifacts | Blind final quality judgments; independent second-rater sample if available. Agree evaluation workload before asking for a large batch | Report the measured win, loss or inconclusive result. Claim superiority only for the tested model/task/domain with adequate evidence; unresolved uncertainty is not a win |

Planning envelope: roughly1-3 focused work sessions per sprint after its inputs are
ready. This is a scheduling estimate, not a runtime or delivery promise. Free-GPU
availability, source access, human decisions and comparator access are explicit
dependencies. A sprint ends at a defined result or a documented gate, not because
a fixed number of calendar days elapsed.

**First model and experimental comparison**

Keep the pinned FashionSigLIP encoder initially. Use garment-wide features for
silhouette, and garment-wide plus hip/thigh features for surface. Regional position
must remain meaningful; knee fading cannot stand in for thigh fading. Start with
two small trainable projections to reduce the risk of fitting a tiny label set.
If frozen features discard needed details, head adaptation may fail; the subsequent
last-block experiment tests that limit rather than assuming it is solved.

| Experiment | Inputs / adaptation | Purpose |
|---|---|---|
| E0 | Frozen encoder, garment-wide view | Current retrieval reference on the same prepared data |
| E1 | Same frozen encoder, garment-wide+regional views; no learned heads | Isolate what input/local evidence changes; select any aggregation only on development |
| E2 | Same views, two axis-supervised trainable projections | Isolate task-specific adaptation over E1 |
| E3, conditional | Same accepted data/views, last vision block adaptation | Test whether changing visual features adds value after the head experiment |
| G | Specified strong general multimodal model, same evidence and candidate pool | Quality comparator; exact available model/version and access still need verification |

Prepare G's inputs/prompt and freeze its development comparison before selecting
the adapted recipe; run the same frozen prompt on the final test. G gets equivalent
garment/region views, a cross-product appearance instruction and uncertainty options.
Do not use small Qwen tag accuracy as its proxy, force an identity-matching prompt,
or give it poorer images. Compare ordering within a shared pool separately from
the complete retrieval pipeline. A reranker cannot recover a missing candidate.

Source-group splits precede pair construction. Existing viewed/trained material
remains development data; known links and capture separation are not certified
product independence. Preserve the historical validation and reservation overlays.
Build the new protocol's train/development/test groups explicitly; do not relabel
the current three boards as a final test.

**Data, annotation and human workload**

- Start from already acquired material and inspected rectangles. Inventory larger
  originals in the existing archive before seeking another broad download. Keep
  low-resolution examples for readable broad cues; they cannot certify weave or
  tiny wash details. New source access/rights remain source-specific checks.
- Use a staged supply target: a development subset with plausible alternatives,
  then a few hundred readable observations if the pilot needs more variety. These
  are working ranges, not minimum scientific requirements or promised availability.
- A first label-feasibility target is at least ten varied anchor groups with
  useful relationships for each trained axis. Three anchors/six preferences are
  insufficient for a quality claim. Judge evidence and coverage, not generated
  triplet count. Repeated combinations do not add independent examples.
- Codex handles extraction, crop proposals, metadata joins, duplicate/group checks,
  candidate suggestions, training, experiment tracking and analysis. Model-produced
  labels remain weak; teacher agreement is not independent human truth.
- Human judgments define relative closeness and acceptance. Retain A/B/tie/neither/U
  per axis without inventing absolute grades. Existing joint judgments stay joint.
  Relative preferences may train ranking, but cannot be used directly as nDCG grades.
- Use right-side tabs for inspection and zoom. Confirm actual visibility before
  requesting answers; a queued request does not clear the presentation gate. Reuse
  the prepared artifacts and existing packet workflow before building more UI.
- Ask5-10 decisions per interaction, with neither/U available. Prioritize close
  confounders and model disagreement while keeping some random coverage. Report
  useful relationships and actual human time when measured. Do not hide total work
  by splitting an unexpectedly large annotation job into many small requests.

**Evaluation and success**

Development evaluation supports selecting checkpoints, region rules, aggregation
and prompts; final evaluation must be untouched by those choices. Preserve complete
human grades for fixed pools when computing nDCG@5 and precision@5. Assess both
axes and directly judged overall acceptability; do not average away a major failure.

A later20-30-query final pilot is a planning range, not evidence of sufficient
statistical power. Before it starts, report the number of queries, pooled candidates,
axes, repeats and raters, and the resulting total human workload. Use a small
complete-pool subset for graded ranking and a separate blind comparison of the
systems' returned results where that answers the research question more efficiently.
Do not mix those endpoints or claim full-gallery recall from incomplete pools.

Success requires matched quality evidence over G and the frozen reference on new
groups, accompanied by axis/per-query errors and paired uncertainty at query/group
level. Report wins, ties, neither and unknown rather than a cherry-picked win rate.
Measure the predefined challenging slices and representative overall cases; the
former alone cannot support a broad superiority claim. A single-rater pilot can
establish feasibility; broader human claims require independent judgments.

No fixed improvement percentage is promised or retrospectively chosen. If an
external claim is intended, predeclare the primary endpoint and evidence threshold
after the development pilot and before touching the final test. If quality is tied,
efficiency may still be a finding, but does not satisfy the primary ambition.

**Investigation backlog, triggered by evidence**

| Observation | Investigate next | Artifact / decision |
|---|---|---|
| Mostly neither or no convincing alternatives | Candidate coverage, source diversity and close-product supply | Coverage report; add the missing examples before training |
| Wash is unreadable | Original image supply, crop visibility and spatial resolution | Resolution/region audit; limit the claim or improve inputs |
| Surface gain but silhouette regression, or reverse | Axis label leakage, feature sharing and aggregation | Per-axis error table; adjust the implicated component |
| Better fitting but no validation gain | Anchor diversity, group leakage, label errors and model capacity | Data/split audit, then a separately controlled capacity change |
| Reasonable encoder ranks but G reranks much better | Cross-image/local interactions and difficult comparisons | Targeted local ranking experiment; investigate relevant reranker methods |
| Apparent win only with AI-generated labels | Teacher bias, shared evaluator and test contamination | Independent human audit before any superiority claim |

Refer to the [existing literature review](LITERATURE_REVIEW_20261030.md) when choosing
the next intervention. Add a focused source/code investigation when it would change
a decision; do not restart a general paper survey at every iteration.

**Sprint closure and immediate work**

At each boundary use [the mandatory review](SPRINT_REVIEW.md): approved plan versus
actual step, new quality evidence, unresolved limits/feedback, next investigation
and exact human gate. Update current state and brief in Korean. Separate acquisition,
software, annotation, fitting and quality evidence. Keep private data out of Git.

Immediate work order: verify that the prepared boards can actually open in the
right-side panel; prepare the scoped-label import/training contract and grouped
input audit in parallel; then collect the existing six answers once the researcher
resumes that gate. The earlier request to defer questions is respected. Planning
does not fabricate missing labels, authorize paid APIs/new agreements, or imply new
training results. Existing free remote-compute authorization continues to apply.
