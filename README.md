# Denim Atlas

A small research project on matching different denim products by photographed
silhouette, color, tone, washing and fading. 개인 취향 분석이나 앱 제작보다,
외관 매칭 모델의 적응과 검증에 집중합니다.

**Snapshot: 2026-11-09 — direct-choice retest measured; silhouette closure/write-up proposed, research gate pending.
Independent matching-quality improvement and superiority to a strong general model
have not been demonstrated.**

The fixed-pool, single-rater comparison covers30 wearing anchors,90 pairs and9
delayed repeats, with no new training. Human preference agreement (silhouette /
surface;95% anchor-bootstrap CI) is FashionSigLIP69.8%[57.7,82.0] /
67.5%[53.7,81.5], CLIP62.3%[47.2,76.4] /57.5%[40.0,73.2], and
DINOv266.0%[51.8,80.0] /65.0%[46.2,81.8]; random agreement is50%.
Exact repeat agreement is8/9 and3/9 respectively. The approved reliability gate
fails for surface, so these are descriptive measurements and adaptation is paused.
Model-to-model nDCG differences are inconclusive. Six high-resolution natural
wearing anchors and24 low-resolution catalog wearing anchors confound resolution
and capture setting; all gallery inputs are low-resolution catalog photos.
Pure catalog query and strong general multimodal comparisons remain unmeasured.
Raw photos, features and human judgments remain private. [Protocol/results](docs/SPRINT_REVIEW.md).

A separate nine-anchor direct-choice diagnostic adds18 axis choices. Strict-choice
agreement is FashionSigLIP5/7,CLIP2/7,DINOv22/7 for silhouette and1/5,4/5,3/5 for
surface. Human ties/unknowns are excluded. Six surface anchors were excluded from
the main analysis, so these small diagnostic counts cannot be compared directly
with the main rates or used to establish a new model ranking. The original
reliability gate remains pending; this supplement does not validate retest stability.

The current primary endpoint is human preference concordance on matched candidate
comparisons; historical three-candidate nDCG is retained only as a descriptive
record. Direction-repeat checks reuse one repeated candidate against two fixed
first-session candidates, so they do not identify an independent human ceiling.
A single pinned open-weight general visual-language comparator is prepared for
free private Kaggle evaluation; execution completed under the approved AB/BA protocol.

The [revised development plan](docs/DEVELOPMENT_PLAN.md) puts evaluation coverage
and an exact strong-model comparator before another adaptation trial. Existing
Sprint 2 code and result artifacts are recorded in commit `1bcc00b`; the repository
revision containing this README also includes the subsequent documentation updates.

## Current evidence

| Item | Verified state |
|---|---|
| Latest experiment | Frozen FashionSigLIP plus separately trained silhouette/surface projection heads; one fixed 200-step run on Kaggle T4 |
| Development result | Frozen garment, frozen regional and trained-head variants each agree with the machine teacher on 2/3 preferences per axis; no net gain |
| Input | 27 photographs / 54 garment and hip-thigh views; train 18 / development 9; 3 development anchors |
| Supervision | 20 conversational-assistant decisions: 13 train constraints, 6 development constraints and 1 excluded neither. Machine supervision, not human truth |
| Source detail | All 1,200 cached GLAMI originals, including 562 provisionally accepted observations, are 228x298. Fine weave and tiny wash details are unresolved |
| Independence | Known source/file/pixel groups are separated. Certified product independence and adequate independent appearance evaluation are not established |
| General-model comparison | Not executed. Exact strong comparator version/access and independent evaluation truth remain unresolved |

## Sprint 2: matched controls and result

The pinned backbone is `Marqo/marqo-fashionSigLIP`, revision
`c56244cc94f92419e8369fa71efdaf403b124ce8`. It stayed frozen. The adapted variant
learns bias-free 64-D projections for silhouette and surface, with 147,456 trainable
parameters. Both use the same frozen packet and grouped folds.

These counts measure agreement with frozen machine preferences on the **same
three development anchors**. They are not human-rated retrieval quality.

| Variant | Development silhouette | Development surface |
|---|---|---|
| E0 — garment-wide frozen features | 2/3 | 2/3 |
| E1 — frozen garment + hip/thigh features | 2/3 | 2/3 |
| E2 — untrained projection control | 1/3 | 2/3 |
| E2 — trained projections | 2/3 | 2/3 |

Silhouette fixes one preference and regresses another; surface winners remain
unchanged. Training fits its constraints, but development agreement does not improve.
The development set has **zero axis-conflicting cases and zero wearing photos**;
it cannot establish generalized axis separation or wearing-to-catalog robustness.
No checkpoint or hyperparameters were selected from the development results.

[Experiment, fitting measurements and failures](docs/REGIONAL_AXIS_PILOT.md) ·
[Configuration fixed before execution](docs/verification/sprint2_preflight_20261105.json) ·
[Aggregate results and provenance](docs/verification/sprint2_results_20261105.json) ·
[Execution checks](docs/verification/sprint2_checks_20261105.json).

Earlier new-query human development nDCG@5 declined from 0.3841 to 0.3513; that
small single-rater check was not an adequate independent product-group test.
Historical fitting and title-cut proxy gains remain in the
[fit study](docs/FIT_PROXY_EXPERIMENT.md) and [human continuation](docs/HUMAN_ROUND2.md).
They are not evidence of improved appearance matching.

## Task definition and next work

Keep two inspectable axes: **silhouette** (visible volume and upper-leg/knee/hem
profile) and **surface** (photographed color/lightness/cast, fade contrast and
pattern/location, distressing). Preserve observed lighting and wear. Product
identity and shared retail labels are not automatic positives. Perceptual
acceptance tolerances remain unvalidated. [Working definition](docs/SIMILARITY_DESIGN.md).

| Stage | State / next deliverable |
|---|---|
| Sprint 1 — usable regional inputs | Execution recorded; research gate pending independent human evaluation and readable data |
| Sprint 2 — first axis-head adaptation | Pipeline check executed; quality hypothesis inconclusive on 3 machine-judged anchors |
| Sprint 3 — evaluation and strong comparator | Next: readable, protected evaluation groups, axis-conflicting/wearing cases, frozen judgments and exact model/access/prompt; matched frozen/comparator results before more adaptation |
| Sprint 4 — controlled improvement | Change one implicated component, retain controls and investigate regressions |
| Sprint 5 — independent comparison/release | Freeze the recipe before final evaluation; publish only conclusions and artifacts supported by evidence and rights |

Training annotation remains delegated to the visual assistant. Machine evaluation
must be identified as such; labels from the comparator itself cannot establish
independent superiority. Human-quality claims require independent human evidence.
No large manual training grid, paid API call or color-only replacement objective
is assumed by this plan.

## Code, checks and reproducibility limits

Start with these files when reviewing the current implementation:

- [Regional feature extraction, controls, training and checkpoint check](scripts/regional_experiment.py)
- [Axis supervision, source/crop provenance and grouped-fold validation](scripts/regional_supervision.py)
- [Experiment metric/cache tests](tests/test_regional_experiment.py) and [supervision tests](tests/test_regional_supervision.py)
- [Current handoff](PROJECT_STATE.md), [revised plan](docs/DEVELOPMENT_PLAN.md) and [recorded sprint findings](docs/SPRINT_REVIEW.md)

```sh
python -m unittest discover -s tests -v
```

84 local tests passed before the Sprint 2 run. The actual CUDA run verified finite
parameter updates, exclusion of development scores from the training loss and
saved-head prediction restoration. Local recomputation of E0/E1 outcomes matches
the GPU report. These checks establish execution behavior, not matching quality.

Raw photographs, judgments and weights remain private. An external reader can
inspect source, fixtures and aggregate results but cannot independently rerun the
private-data experiment from this repository alone. Model processing stays on
remote Kaggle CUDA; no model weights are downloaded to the old laptop.

Codex assisted with code, source investigation, visual screening and execution.
The researcher supplied the historical joint human judgments. The latest axis
judgments were created by this Codex conversation's visual assistant; no separate
ChatGPT API was invoked and its exact checkpoint is unexposed. Legacy joint labels
remain joint. The 96 rejected Qwen attribute drafts remain outside training.

GLAMI's publisher card states Apache-2.0; this project has not independently cleared
every seller image or derived-checkpoint release. Source/model terms apply
separately. Raw material and model artifacts have not been published.

Qwen3.5-9B: **이 입력 형식에서 순서 불일치 71~78%로 비교 불성립, 범용 모델 대비 우열 미측정.**
The64/90 silhouette and70/90 surface order-disagreement outcomes invalidate a
capability ranking from this run. Order-consistent subsets such as14/15 are selected
samples and are not evidence of superiority. Raw outputs remain execution diagnostics.
R2 proceeds only to a separately approved direct-direction retest block,with no training.

That separate direct-choice block now has both passes:18 comparisons across16
known reference source groups,with109 minutes between passes and224 input.
It is restricted to comparisons whose original scores were non-tied on both axes.
Human direction-repeat reference C is17/18(94.4%) for silhouette and13/14(92.9%)
for surface;first/retest unknowns are0/18,0/18 and4/18,4/18 respectively.
These are conditional reliability references,not universal performance ceilings.

| Direct-choice retest only | Silhouette:first choice | Surface:first choice | Silhouette:stable subset | Surface:stable subset |
|---|---:|---:|---:|---:|
| FashionSigLIP |16/18|9/14|15/17|9/13|
| CLIP |11/18|11/14|10/17|10/13|
| DINOv2 |12/18|9/14|11/17|8/13|

The fixed silhouette rule triggers a closure/write-up proposal:FashionSigLIP88.9%
is5.6 percentage points below C,within the10-point margin. This is not an automatic
project closure or a claim of optimal matching. Surface passes the predeclared
measurement thresholds(C>=80%,retest unknown<=30%) on this block;no learning is
automatically authorized. Stable subsets are diagnostic only. Original score-based
results remain separate,unchanged. No fresh-product or fine-washing quality claim.
