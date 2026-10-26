# Denim Atlas

**Fine-tuning a pretrained vision encoder to retrieve denim with similar visible appearance across different products.**

사진 속 데님의 색·톤·페이딩·워싱·실루엣을 비교하는 작은 ML 연구 과제입니다. 개인 취향, 원래 원단 색 복원, 모바일 앱은 현재 범위에 포함하지 않습니다.

## Current snapshot — October 26, 2026

| Area | Verified state |
|---|---|
| Model / compute | Marqo fashionSigLIP inference, synthetic backward and checkpoint checks passed on Kaggle T4 |
| Evaluation | Fixed-pool nDCG@5, strict candidate validation and product/duplicate/image split checks implemented |
| Baselines | Cosine B0 and mean-RGB control B1 implemented; ranking-to-evaluation CLI tested on synthetic vectors |
| Local tests | 39 passed on Python 3.12; includes clear-grade training triplets, provenance and evaluation safeguards |
| Data | 900 images audited and thumbnail-inspected; ABO 600 excluded as unsuitable. GLAMI 24 clear denim crops visually reviewed by Codex; remaining crop/group review pending |
| Real-image execution | 24 reviewed GLAMI crops encoded on T4; 768-D features and exploratory B0/B1 neighbor boards saved |
| Calibration nDCG@5 (B0 / B1) | Q2: **0.641 / 0.640**; Q3: **0.530 / 0.447**. Single-rater pilot, 24 candidates; Q1 excluded |
| First fine-tuning | Last vision block, 7,087,872 parameters, 40 real-label steps. Training hinge loss **0.0794 → 0.0185**; checkpoint weight restoration passed |
| Held-out quality | **Not measured**; current three queries are now training data, with product groups and independent splits pending |
| Human judgments | First single-rater calibration export received: 75/75 trials; 71 usable unique pairs, one conflicting repeat pair excluded. No held-out quality result |

Wearing-photo supply follow-up: a bounded Commons pilot acquired 24 attributed
CC0/CC BY previews. A user-authorized Unsplash Lite audit processed 25,000 photo
records, found 293 text candidates and privately inspected 24 previews on Kaggle.
Neither new pilot is training-ready. See [wearing-photo evidence and limits](docs/WEARING_DATA_PILOT.md).

Calibration numbers above were recorded before training. The first fine-tuning run then used the same 27 images and clear human judgments to test actual adaptation; its loss decrease is training-set fitting, not unseen retrieval improvement. No further standalone starting-model validation is planned. DeepFashion applications remain separate access requests.

## Human and AI contributions

This is an AI-assisted research project. Codex assisted with implementation, tests, source investigation, preliminary visual screening/crop review and experiment execution. The researcher supplied all 75 appearance-relevance judgments through a rank-blind sheet; AI screening is not human ground truth. The researcher owns study decisions and result interpretation. Single-rater calibration is reported separately from future independent evaluation.

## Research question

Can human appearance judgments improve ranking on unseen product groups over the frozen starting checkpoint and a simple color control?

Match the visible garment, including lighting and wear. Different products can match; same-product identity is not an automatic positive. Freeze product/duplicate groups and splits before constructing training pairs. Compare identical fully judged pools using nDCG@5 with gain `2^grade - 1`; uncertain labels are not zero. Choose weights/checkpoints on validation only.

## Run the lightweight checks

```sh
python -m unittest discover -s tests -v
python scripts/run_baselines.py --benchmark data/private/validation.json --features runs/features.json --color-weight 0.5 --output runs/baselines-validation-w05
```

The second command needs reviewed benchmark/features; paths and weight are examples. Synthetic fixtures are included in tests, not claimed as research data. Scoring/evaluation use the standard library. Image/model processing stays on remote compute; do not download weights to the old laptop.

## Next milestone

Expand and preprocess permitted denim data, collect the needed human judgments, and iterate fine-tuning. Keep the first pilot's three training queries out of future held-out claims; review product/duplicate groups before splitting the expanded data. Work is paused at the researcher's request for folder organization.

## Documentation and evidence

- [Research design, project history, model acquisition and recorded measurements](docs/RESEARCH.md)
- [Benchmark schema, human-judgment rubric and evaluation](docs/EVALUATION.md)
- [Single-rater calibration packet and next labeling step](docs/JUDGMENT_ROUND1.md)
- [First real-label fine-tuning run](docs/TRAINING_PILOT.md)
- [Open-source reuse review and adoption decisions](docs/OPEN_SOURCE_REVIEW.md)
- [Remote feature extraction and B0/B1 runbook](docs/BASELINES.md)
- [Dataset access checks and contingency](docs/DATA_ACCESS.md)
- [Alternative datasets: acquisition and application record](docs/DATASET_SEARCH.md)
- [900-image audit, exclusions and real-image pilot](docs/SCREENING_PILOT.md)
- [Next DeepFashion2 import](docs/NEXT_DATA_RUN.md)
- [External-feedback audit: addressed and outstanding](docs/FEEDBACK_AUDIT.md)
- [Current project state](PROJECT_STATE.md) · [Recovery provenance](docs/RECOVERY.md)

The original workspace was partially recovered from saved Kaggle code/output. The current evaluator is newly implemented; lost planning/legacy UI files are not claimed recovered. GLAMI's publisher card labels the dataset Apache-2.0; this project has not independently established every seller image's rights or cleared release of derived checkpoints. Raw images, judgments, correspondence and weights remain private. Publication of model artifacts needs a separate rights review; upstream image/model terms apply independently.
