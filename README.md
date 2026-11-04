# Denim Atlas

A small research project on matching different denim products by photographed
silhouette, color, tone, washing and fading. 개인 취향 분석이나 앱 제작보다,
외관 매칭 모델의 적응과 검증에 집중합니다.

**Snapshot: S2-2026-11-05 — Sprints 1 and 2 are complete as experiments.
Independent matching-quality improvement and superiority to a strong general model
have not been demonstrated.**

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
| Sprint 1 — usable regional inputs | Completed for a small machine-supervised pilot; no independent ground truth established |
| Sprint 2 — first axis-head adaptation | Completed with no development-agreement gain |
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
