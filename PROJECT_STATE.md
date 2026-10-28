# Denim Atlas — 2026-10-29

Goal: cross-product similarity of observed denim color/tone, wash/fading and silhouette. No taste profiling, color restoration or app UI.

## Completed this sprint

- Audited current labels: no structured observed-color/wash targets. Extracted five explicit weak title-cut classes from 160 of 347 previously screened images.
- Grouped known item/pixel/title-family links; initial split 121 train / 39 validation. Fine-tuned the last FashionSigLIP vision block, 120 FP32 updates, lr 1e-6, balanced cross-source triplet batches.
- Same 39-image proxy validation: frozen class-macro nDCG@5 0.4174; three training-order seeds 0.5189 / 0.5182 / 0.5157. Mean 0.5176. Same-seed metrics repeat; bitwise block digests differ.
- Screened another 239 acquired images, provisionally accepted 215. Inventory: 562 accepted candidates, 375 explicit weak cut labels. Reserved 3 linked images; expanded train333 / exact original validation39. Same 120 updates: proxy score 0.4990.
- Reused 51 existing human grades: original frozen baseline 0.3888; small fit model 0.4129, expanded fit model 0.4053. No new training labels or checkpoint tuning from human answers; three development queries are not a fresh test.
- 52 local tests pass; all completed training runs passed same-kernel checkpoint restoration. Weights/images stay private and remote; no pending compute job.

## Current human-input gate

Two selected A/B appearance comparisons, not a full grid. Private sheet: `data/private/fit_spot_audit_20261029/spot_audit/selected_contact.jpg`. Await A / B / tie / neither / uncertain for display rows 1 and 2.

Record answers against `human_request.json`: display1 maps to original question2; display2 maps to question4 of packet `7906891dbae0302d489a36b9f435fb971f4e97f87c8f9ad2c34cd2d6b98762b6`. Use `model_mapping_private.json` only after human replies. Keep relative judgments separate from absolute grades; selected cases cannot estimate population quality. Two obvious color-mismatch cases were not sent or auto-labeled.

Next: interpret this focused feedback, then address observed-color/wash supervision and wearing-photo transfer. Keep fit-only weights experimental. Source-cut labels are noisy; product identities/splits are not independently certified. More data at the same update budget did not beat the smaller run. Seller-image/model publication rights and access-request status remain unresolved.

[Experiment and reproducibility](docs/FIT_PROXY_EXPERIMENT.md) · [Methodology](docs/METHODOLOGY_BENCHMARK.md)
