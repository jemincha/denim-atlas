# Denim Atlas

**Independent matching-quality improvement has not been demonstrated.**

사진 속 데님의 실루엣과 색·톤·워싱·페이딩을 기준으로, 서로 다른 상품의
외관 유사도를 학습하는 연구 프로젝트입니다. 개인 취향 분석, 원래 원단 색
복원과 모바일 앱 제작은 현재 범위에 포함하지 않습니다.

## Current evidence — November 5, 2026

| Question | Current answer |
|---|---|
| Does adaptation improve independent product-group matching quality? | Not established. No adequate independent appearance benchmark yet |
| Does it outperform a strong general multimodal model? | Not measured. Comparator version/access and independent evaluation truth remain unresolved |
| Latest controlled result | Frozen garment, frozen regional and trained axis-head models each agree with the machine teacher on2/3 development preferences per axis; no net gain |
| Latest data |27 photographs /54 garment and hip-thigh views; train18/development9,3 development anchors. Known source/file/pixel groups are separated; certified product independence is not established |
| Input limit | All1,200 cached GLAMI source images are228x298, including562 provisionally accepted observations. Fine weave and tiny wash details are unresolved |
| Supervision limit |20 conversational-assistant judgments yield13 train/6 development constraints;1 neither is excluded. They are weak machine supervision, not human truth; the teacher checkpoint is unexposed |

## Latest comparison

FashionSigLIP remains frozen; the adapted variant learns separate silhouette and
surface projections. These counts measure agreement with the frozen machine
preferences on the same3 development anchors, not human-rated retrieval quality.

| Model | Development silhouette | Development surface |
|---|---|---|
| E0 garment-wide frozen features |2/3|2/3|
| E1 frozen garment+regional features |2/3|2/3|
| E2 untrained projection control |1/3|2/3|
| E2 trained projections |2/3|2/3|

Silhouette fixes one preference and regresses another; surface winners do not
change. Development has no cases with different winners between axes and no
wearing photographs. It cannot establish generalized axis separation or
wearing-to-catalog robustness. [Full results, fitting measurements and failure analysis](docs/REGIONAL_AXIS_PILOT.md).

An earlier single-rater, new-query human development check declined in nDCG@5
from0.3841 to0.3513. It is not a sufficiently independent product-group test.
Training-set fitting and title-cut proxy gains are recorded in the
[experiment history](docs/RESEARCH.md), [fit study](docs/FIT_PROXY_EXPERIMENT.md)
and [human continuation](docs/HUMAN_ROUND2.md); they are not appearance-quality gains.

## Task and next evidence gate

Compare two separately inspectable axes: visible volume/leg profile, and photographed
color/lightness/cast plus fade contrast/pattern/location and distressing. Preserve
observed lighting and wear. Product identity and shared retail labels are not
automatic positives. [Working definition and unresolved tolerances](docs/SIMILARITY_DESIGN.md).

Before another adaptation trial, strengthen an evaluation set kept outside training,
including axis-conflicting alternatives and wearing views; establish the exact
strong general-model comparison route on the same images and candidate pools.
Freeze judgments and comparison rules before inspecting system rankings. Separate
teacher reproduction from independent quality, and change one experimental factor
at a time. The latest no-gain run does not justify a larger model or a parameter sweep.

Training annotation has been delegated to the visual assistant. Large manual
training grids will not be reintroduced by default. Independent evaluation truth
is still a separate requirement for a credible superiority claim.

## Reproduction and provenance

Code and lightweight checks are available; raw photographs, judgments and weights
remain private. Model execution runs on Kaggle CUDA, not the laptop.

```sh
python -m unittest discover -s tests -v
```

Software checks and saved-checkpoint restoration establish execution correctness,
not matching quality. Model/config/input hashes and actual controls accompany the
[regional experiment](docs/REGIONAL_AXIS_PILOT.md).

Codex assisted with implementation, visual screening, source investigation and
experiment execution. The researcher supplied the historical three rounds of joint
human judgments. The latest axis-specific labels were created by this Codex
conversation's multimodal visual assistant, with no separate ChatGPT API call.
Legacy joint labels remain joint; they cannot be retrospectively split into axes.
Rejected Qwen attribute drafts remain outside training.

[Current state](PROJECT_STATE.md) · [Plan](docs/DEVELOPMENT_PLAN.md) ·
[Sprint findings](docs/SPRINT_REVIEW.md) · [Evaluation protocol](docs/EVALUATION.md) ·
[Supervision input contract](docs/SPRINT1_INPUT_CONTRACT.md) ·
[Research history](docs/RESEARCH.md).

GLAMI's publisher card states Apache-2.0; this project has not independently cleared
every seller image or derived-checkpoint release. Source/model terms apply
separately. Raw material and model artifacts have not been published.
