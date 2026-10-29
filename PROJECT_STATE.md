# Denim Atlas — 2026-10-29

Goal: cross-product similarity of observed denim color/tone, wash/fading and silhouette. No taste profiling, color restoration or app UI.

## Completed this sprint

- Audited current labels: no structured observed-color/wash targets. Extracted five explicit weak title-cut classes from 160 of 347 previously screened images.
- Grouped known item/pixel/title-family links; initial split 121 train / 39 validation. Fine-tuned the last FashionSigLIP vision block, 120 FP32 updates, lr 1e-6, balanced cross-source triplet batches.
- Same 39-image proxy validation: frozen class-macro nDCG@5 0.4174; three training-order seeds 0.5189 / 0.5182 / 0.5157. Mean 0.5176. Same-seed metrics repeat; bitwise block digests differ.
- Screened another 239 acquired images, provisionally accepted 215. Inventory: 562 accepted candidates, 375 explicit weak cut labels. Reserved 3 linked images; expanded train333 / exact original validation39. Same 120 updates: proxy score 0.4990.
- Reused 51 existing human grades: original frozen baseline 0.3888; small fit model 0.4129, expanded fit model 0.4053. No new training labels or checkpoint tuning from human answers; three development queries are not a fresh test.
- All completed training runs passed same-kernel checkpoint restoration. Weights/images stay private and remote; no pending compute job.

## Follow-up and candidate-pool diagnosis

The two selected comparisons were answered **neither / neither**. Private responses: `data/private/fit_spot_audit_20261029/spot_audit/responses_20261029.json`; aggregate: `docs/verification/glami_fit_spot_audit_results_20261029.json`. No absolute grade0 labels, A/B ties or triplets inferred. The researcher further reports almost no overall resemblance in either displayed case. Specific facet causes remain unspecified; no additional explanation is required.

- Fashionpedia metadata audit complete: 294 attributes, 314 pants; jeans109 / washed68 / distressed21 (overlapping pants counts, not approved denim). No photographed-color or fine fading-strength/location labels established; no images downloaded.
- Qwen3-VL-2B-Instruct image-only pilot complete: 24 previously reviewed images, pinned revision/weights, T4 inference 108.81s / 4.078GiB. Original parser accepted22; two view/detail contract violations. Three more contradicted no-fading with faded whiskers; revised consistency pass19. Unknowns absent and detail labels repetitive. No human attribute-accuracy labels; no training/reranking or large-scale annotation performed. Keep these descriptions unverified and do not scale.
- 70 local tests pass. No pending compute jobs. Retrieval backbone remains FashionSigLIP; fit-only weights remain experimental.

The follow-up closes the mismatch question: overall resemblance was rejected; no personal weights or facet-specific cause inferred. A private CPU run reused 372 cached embeddings, expanding each selected query from 38 eligible validation candidates to 371 cross-group candidates. Both expanded-gallery top-1 choices are identical before/after fit adaptation (top-8 overlap 8/8 and 7/8). Training images are allowed in this diagnostic; it is not held-out evaluation and does not cover all 562 accepted candidates. No human acceptance or absence of a suitable match established. [Evidence](docs/verification/gallery_diagnosis_20261029.json).

The researcher clarified that the joint prompt led to rejection whenever either silhouette or surface differed substantially. Old grades do not reveal the failed axis and are not decomposed. Audit found: one joint human grade, one shared embedding, cut-only triplets unconstrained by surface, and no validated surface objective.

Implemented: new packet CLI defaults to schema2 with separate silhouette/surface scores on the same image pair; independent U/repeats/conflicts; explicit-axis analysis; legacy joint trainer rejects these records. Historical packets/API defaults and grades stay intact. 60 tests plus actual browser download/import and 390px layout checked using engineering fixtures only. [Separation audit](docs/AXIS_SEPARATION_AUDIT.md).

Next: credible axis-specific supervision and diagnostic contrasts (same cut/different surface and different cut/similar surface), then an explicit axis-conditioned training objective. Two heads are a proposal, not a trained model. Do not expand fit-only training, train on unverified VLM descriptions, infer positives from proximity, or require both axes to match before collecting axis-specific evidence. No pending compute job. The eight-image expansion audit below is the current human gate. Raw model outputs/statuses and revised validator remain separate; consistency passes are not visual accuracy.

Protected-dataset access and source-image/model-publication rights remain unverified. Conservative source groups do not certify independent products.

Working design: [attribute representation and similarity](docs/SIMILARITY_DESIGN.md). Two main axes, eight initial attribute groups; volume/profile and color/lightness separated; fading recorded as observed contrast/pattern/location rather than inferred process. Ordinal anchors, tolerances and axis-conditioned heads are proposed, not fixed/trained. No new annotations, training or quality measurements for this design review.

[Appearance pilot](docs/APPEARANCE_ANNOTATION_PILOT.md) · [Fit experiment](docs/FIT_PROXY_EXPERIMENT.md) · [Methodology](docs/METHODOLOGY_BENCHMARK.md)

## Attribute feasibility execution

`prepare_attribute_audit.py` built a draft inventory: 562 catalog observations plus 3 existing Commons crops; 375 weak retail-fit tags and 24 machine drafts each for color, lightness and tone. No labels certified or promoted to training. All 24 pilot image hashes verified and visually inspected by Codex. Coarse color remains a calibration candidate; lightness collapsed to medium20/dark4, no light or unknown; tone lacks anchors. Rejected wash descriptions stay excluded.

The six anchor answers were received: five explicit family values, six brightness values. Image5 raw-denim wording does not identify family; leave that field unassigned. Image6 very-light wording is preserved and mapped to the existing light bin. Original VLM agreement: family5/5 comparable, brightness2/6; selected development-anchor counts only. No relevance labels or training eligibility inferred.

Two bounded, pinned-model T4 inference retries completed on the same 18 unjudged targets, excluding all six anchors. Text-only brightness dark6/medium12/light0; with five verified reference images dark6/medium9/light3. Four family outputs changed neutral->blue with references. Accuracy on these targets is unknown; keep variants/fieldwise drafts unverified. Original exact-fence parsing failure and separate normalization are both preserved. No optimizer updates or model weights on laptop.

The three follow-up answers are recorded: blue/light, blue-black/dark, blue/medium. Visual-reference outputs agree3/3 per attribute; text-only2/3 per attribute. Selected development evidence only. The blue-black answer resolves one provisional Codex neutral interpretation in favor of the reference-context prediction; the earlier fieldwise-source draft is not adopted.

Fixed five-anchor 96-image weak-label expansion completed: 16 per each of six source-tag sampling strata, seed131, 96 distinct linked groups. Full source-metadata/item/title/pixel links protect validation39, reserves3 and prior pilot observations; 55 reviewed images excluded. Four additionally selected legacy-human-pool-linked images are reserved from any later training by a separate overlay. No retrieval-model training performed.

All96 outputs are schema-valid, unverified drafts: blue81/neutral15; light16/medium58/dark22; no unknowns. Codex inspected four sheets and flagged possible other-color and brightness-boundary problems without assigning ground truth.

Current human gate: eight photos fixed before inference (seed197; one per sampling stratum plus two random remaining), under `data/private/attribute_expansion_20261029/`; family and brightness only, predictions hidden. All96 remain outside training; no pending compute jobs. 70 tests pass. [Execution and limits](docs/ATTRIBUTE_AUDIT.md).
