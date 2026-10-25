# Denim Atlas

**Fine-tuning a pretrained vision encoder to retrieve denim with similar visible appearance across different products.**

사진 속 데님의 색·톤·페이딩·워싱·실루엣을 비교하는 작은 ML 연구 과제입니다. 개인 취향, 원래 원단 색 복원, 모바일 앱은 현재 범위에 포함하지 않습니다.

## Current snapshot — October 25, 2026

| Area | Verified state |
|---|---|
| Model / compute | Marqo fashionSigLIP inference, synthetic backward and checkpoint checks passed on Kaggle T4 |
| Evaluation | Fixed-pool nDCG@5, strict candidate validation and product/duplicate/image split checks implemented |
| Baselines | Cosine B0 and mean-RGB control B1 implemented; ranking-to-evaluation CLI tested on synthetic vectors |
| Local tests | 28 passed on Python 3.12, including audit hashes, duplicate detection and path boundaries |
| Data | 900 images audited and thumbnail-inspected; ABO 600 excluded as unsuitable. GLAMI 24 clear denim crops visually reviewed by Codex; remaining crop/group review pending |
| Real-image execution | 24 reviewed GLAMI crops encoded on T4; 768-D features and exploratory B0/B1 neighbor boards saved |
| Research quality / fine-tuning | **Not measured / not run**; human judgments and independent product groups pending |

The frozen extractor now runs on real denim. A 24-image exploratory pool establishes execution, not retrieval quality or an improvement from fine-tuning. DeepFashion applications remain separate access requests.

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

Expand reviewed GLAMI crops, resolve product/variant/near-duplicate groups, freeze splits and collect cross-product relevance judgments, then record the first scored B0/B1 comparison. Choose the adaptation recipe after inspecting baseline failures.

## Documentation and evidence

- [Research design, project history, model acquisition and recorded measurements](docs/RESEARCH.md)
- [Benchmark schema, human-judgment rubric and evaluation](docs/EVALUATION.md)
- [Remote feature extraction and B0/B1 runbook](docs/BASELINES.md)
- [Dataset access checks and contingency](docs/DATA_ACCESS.md)
- [Alternative datasets: acquisition and application record](docs/DATASET_SEARCH.md)
- [900-image audit, exclusions and real-image pilot](docs/SCREENING_PILOT.md)
- [Next DeepFashion2 import](docs/NEXT_DATA_RUN.md)
- [External-feedback audit: addressed and outstanding](docs/FEEDBACK_AUDIT.md)
- [Current project state](PROJECT_STATE.md) · [Recovery provenance](docs/RECOVERY.md)

The original workspace was partially recovered from saved Kaggle code/output. The current evaluator is newly implemented; lost planning/legacy UI files are not claimed recovered. Upstream image/model terms apply separately. Keep private data, credentials, applications and weights out of Git.
