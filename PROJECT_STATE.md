# Denim Atlas — 2026-10-29

Goal: cross-product similarity of observed denim color/tone, wash/fading and silhouette. No taste profiling, color restoration or app UI.

## Completed this sprint

- Audited current labels: no structured observed-color/wash targets. Extracted five explicit weak title-cut classes from 160 of 347 previously screened images.
- Grouped known item/pixel/title-family links; initial split 121 train / 39 validation. Fine-tuned the last FashionSigLIP vision block, 120 FP32 updates, lr 1e-6, balanced cross-source triplet batches.
- Same 39-image proxy validation: frozen class-macro nDCG@5 0.4174; three training-order seeds 0.5189 / 0.5182 / 0.5157. Mean 0.5176. Same-seed metrics repeat; bitwise block digests differ.
- Screened another 239 acquired images, provisionally accepted 215. Inventory: 562 accepted candidates, 375 explicit weak cut labels. Reserved 3 linked images; expanded train333 / exact original validation39. Same 120 updates: proxy score 0.4990.
- Reused 51 existing human grades: original frozen baseline 0.3888; small fit model 0.4129, expanded fit model 0.4053. No new training labels or checkpoint tuning from human answers; three development queries are not a fresh test.
- 52 local tests pass; all completed training runs passed same-kernel checkpoint restoration. Weights/images stay private and remote; no pending compute job.

## Follow-up and candidate-pool diagnosis

The two selected comparisons were answered **neither / neither**. Private responses: `data/private/fit_spot_audit_20261029/spot_audit/responses_20261029.json`; aggregate: `docs/verification/glami_fit_spot_audit_results_20261029.json`. No absolute grade0 labels, A/B ties or triplets inferred. The researcher further reports almost no overall resemblance in either displayed case. Specific facet causes remain unspecified; no additional explanation is required.

- Fashionpedia metadata audit complete: 294 attributes, 314 pants; jeans109 / washed68 / distressed21 (overlapping pants counts, not approved denim). No photographed-color or fine fading-strength/location labels established; no images downloaded.
- Qwen3-VL-2B-Instruct image-only pilot complete: 24 previously reviewed images, pinned revision/weights, T4 inference 108.81s / 4.078GiB. Original parser accepted22; two view/detail contract violations. Three more contradicted no-fading with faded whiskers; revised consistency pass19. Unknowns absent and detail labels repetitive. No human attribute-accuracy labels; no training/reranking or large-scale annotation performed. Keep these descriptions unverified and do not scale.
- 56 local tests pass. No pending compute jobs. Retrieval backbone remains FashionSigLIP; fit-only weights remain experimental.

The follow-up closes the mismatch question: overall resemblance was rejected; no personal weights or facet-specific cause inferred. A private CPU run reused 372 cached embeddings, expanding each selected query from 38 eligible validation candidates to 371 cross-group candidates. Both expanded-gallery top-1 choices are identical before/after fit adaptation (top-8 overlap 8/8 and 7/8). Training images are allowed in this diagnostic; it is not held-out evaluation and does not cover all 562 accepted candidates. No human acceptance or absence of a suitable match established. [Evidence](docs/verification/gallery_diagnosis_20261029.json).

Next: distinguish gallery coverage from whole-appearance ranking, then establish credible appearance-positive supervision. Do not expand fit-only training, train on unverified VLM descriptions, infer positives from proximity, or request another large rating grid. No pending human question or compute job. Raw model outputs/statuses and revised validator remain separate; consistency passes are not visual accuracy.

Protected-dataset access and source-image/model-publication rights remain unverified. Conservative source groups do not certify independent products.

[Appearance pilot](docs/APPEARANCE_ANNOTATION_PILOT.md) · [Fit experiment](docs/FIT_PROXY_EXPERIMENT.md) · [Methodology](docs/METHODOLOGY_BENCHMARK.md)
