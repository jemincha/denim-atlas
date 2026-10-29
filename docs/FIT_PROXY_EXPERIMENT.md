# Attribute-supervision pilot — October 29, 2026

This is an ASEN-inspired supervision experiment using the existing Marqo FashionSigLIP encoder. It does not reproduce ASEN's architecture or establish full denim appearance quality. No new human labels were required for the automated experiments.

## Reusable signal and data

The acquired GLAMI metadata has no structured observed-tone or wash labels. Explicit source-title terms yielded five noisy catalog-cut classes from the 347 previously screened images: skinny 44, slim 42, straight 49, flared 13, wide-leg/fit 12. Titles with no supported term or conflicting terms stayed unknown; generic `wide pockets` and negated labels are not accepted. These 160 examples support a fit-only proxy, not human silhouette truth or overall appearance positives.

Known item IDs, decoded-pixel hashes and normalized title families are linked before splitting. The initial input contains 159 known source groups, **121 training / 39 validation images**. Validation images rank only the other validation images, excluding their own linked group. These groups are conservative metadata links, not certified independent product identities. There is no pristine test set.

A CPU audit verified all 160 file/pixel hashes and recorded a median 228×298 resolution. Codex inspected five examples per class before training. Catalog and full-body studio views are mixed; apparent slim/skinny/straight boundaries overlap. Labels were retained as weak catalog terminology rather than silently converted to human ground truth. [Audit evidence](verification/glami_fit_supervision_20261029.json).

## Fixed training experiment

- Start from the original pinned pretrained Marqo checkpoint, not the earlier weak-text or human-overfit checkpoints.
- Train only `visual.trunk.blocks.11` (7,087,872 parameters), FP32, AdamW lr 1e-6, weight decay 0.01, gradient cap 1.0, cosine margin 0.1.
- Use five cut classes × four different source groups per batch: 20 images. Within that batch, mean triplet hinge pulls same-cut/different-source examples together and pushes different-cut examples apart. This is a conditional source-cut objective; the negative need not be dissimilar overall.
- Run a fixed 120 updates. Preserve photographed color with white letterboxing; no random crop or color jitter. Dropout remains disabled. No human relevance grades, test feedback or checkpoint selection enters training.
- Verify the loss analytically on remote tensors (expected hinge 0.6 or 0, plus finite nonzero gradients and empty-triplet rejection), guard all updates, and verify same-kernel checkpoint restoration.

Primary proxy metric: average nDCG@5 within each cut class, then average the five class means. Binary relevance means the same source-cut label; this differs from 0–3 human appearance relevance. Flared and wide each have only three validation queries, so their class means are noisy. Precision@5 for those classes is bounded by the small number of positive candidates.

## Results

| Training data / seed | Same fixed validation class-macro nDCG@5 |
|---|---:|
| Original frozen encoder | 0.417377 |
| 121 images, seed 17 | 0.518896 |
| 121 images, seed 31 | 0.518156 |
| 121 images, seed 47 | 0.515748 |
| Three-seed mean / sample SD | **0.517600 / 0.001646** |
| Expanded 333 images, seed 17, same 120 updates | **0.498974** |

All three training-order seeds improved this particular proxy validation score. Their spread is not uncertainty over independent products, datasets or human raters. Same-seed validation rankings reproduced exactly; trainable-block digests differed, so bitwise training reproducibility is not established and tensor-level difference magnitude was not measured.

For the first seed-17 pilot, per-class nDCG@5 was flared 0.483→0.857, skinny 0.363→0.428, slim 0.374→0.352, straight 0.446→0.523, wide 0.421→0.436. The improvement is uneven and disproportionately influenced by the three flared validation images. Expanded-data query-weighted validation mean was 0.4050→0.4578; class-macro was 0.4174→0.4990. Do not present the class-macro as a population estimate.

The first 121-image run's measured training/validation/save segment was 48.05 seconds; repeat segments were 43.66 / 46.51 / 46.49 seconds. The expanded segment was 72.28 seconds. Setup, downloads, source review and job waiting are excluded. Every completed run passed checkpoint restoration. Version 1 of the first job stopped before learning because Windows newline conversion changed the manifest hash; version 2 transmits the original bytes, retaining the provenance guard.

[Initial training](verification/glami_fit_training_20261029.json) · [same-setting repeats](verification/glami_fit_repeats_20261029.json) · [expanded training](verification/glami_fit_expanded_training_20261029.json).

## Expansion with a protected validation set

Another **239 already acquired images** with explicit title-fit terms had not been screened. Codex inspected all six contact sheets: 215 were accepted provisionally, 24 were excluded/uncertain for material evidence, composites, nonstandard construction or unobservable cut. Colored examples were retained when garment construction was readable; this is not a personal color-preference filter or material certification.

The reviewed accepted inventory is now **562 images** (347+215). Of these, 375 have supported title-cut labels. Three new examples linked to the original validation groups are reserved outside training. The expanded experiment therefore uses **333 training / the exact same 39 validation images**. A new source group bridging the fixed training/validation anchors is rejected rather than silently moved. Both old and expanded manifests are preserved privately.

The expanded run holds base checkpoint, preprocessing, sampler, objective, seed and update budget fixed. It improves over the frozen reference but trails the smaller dataset in this run. More data changes composition and gives fewer exposures per example at the same update budget; these results do not establish that additional data is harmful. [Expansion evidence](verification/glami_fit_extension_20261029.json).

## Reuse human evidence before asking for more

The three Commons queries and 17 candidates already judged in round 3 were reused as a frozen development regression check. All 51 pairs remain fully judged; no unjudged gallery image is assigned zero. The comparison now starts from the original frozen encoder, whereas the older round-2 result started from the weak-text parent; those baselines must not be conflated.

| Model | Development mean human-grade nDCG@5 |
|---|---:|
| Original frozen encoder | 0.388788 |
| 121-image source-cut adaptation, original seed-17 pilot | 0.412880 |
| 333-image source-cut adaptation, seed 17 | 0.405258 |

No human labels entered these source-cut runs or checkpoint selection. Three evaluated gallery candidates overlap fit training; queries are different source images, but this is reused development evidence, not a fresh or product-disjoint test. Neither adapted model added a grade >=2 result for the first two queries; the number of grade >=2 results in the third query's top-5 stayed the same. The small increases therefore do not demonstrate useful general search quality.

[121-image development check](verification/glami_fit_relevance_20261029.json) · [expanded development check](verification/glami_fit_expanded_relevance_20261029.json).

## Small human-input gate

A deterministic CPU audit selected one validation query per weak cut class where the frozen and expanded models' top-1 recommendations differ (seed 73). Four classes supplied a case. Two clear visible-color-mismatch cases were removed from the human request without assigning them relevance grades. **Only two ambiguous comparisons** remain. Model names, ranks and weak class labels are hidden in the delivered image; responses are A / B / tie / neither / uncertain. No new annotation website or JSON export is required.

This is selected qualitative feedback, not an unbiased success-rate estimate. Keep relative responses separate from absolute 0–3 relevance grades. The original four cases, private model mapping, displayed-case mapping and image hash are preserved; [preparation record](verification/glami_fit_spot_audit_preparation_20261029.json). The researcher answered **neither / neither** on October 29. Neither model's candidate was acceptable in these two selected cases. The responses remain relative audit records; no absolute grades, A/B tie votes or training triplets were generated. The follow-up reports almost no overall resemblance in either case; no facet-specific cause is inferred and no further explanation is requested. [Recorded feedback](verification/glami_fit_spot_audit_results_20261029.json).

## Reproduction and next limits

`prepare_glami_fit.py` builds weak-cut manifests. Pass `--validation-anchor` when adding images so the original validation queries remain fixed; linked new images are held out. `finetune_glami_fit.py` runs on Kaggle GPU with an exact-manifest review, numeric file IDs, source checksums and a new output directory. `--seed` changes training order while the manifest split stays fixed. All raw images, source titles, inputs and checkpoints remain private. Authorized users can retrieve the exact embedded inputs/source from the named private Kaggle jobs.

The pipeline now supports automatic label-derived training and repeated comparisons without asking the researcher to grade every pair. Color and wash supervision are still missing, source labels are noisy, consumer-photo transfer is weak, and independent product grouping remains unresolved. Keep the fit-only weights experimental; the broader project goal still requires these other signals and genuinely independent evaluation. No new access agreement was accepted or model artifact published in this sprint.

## Follow-up after rejected recommendations

The fit-only weights remain an experimental branch. Do not repeat more fit-only training or request another full rating grid to repair overall appearance. The next bounded audit checks (a) whether public Fashionpedia metadata actually supplies relevant surface labels, without fetching source images, and (b) whether a pinned open vision-language model can describe visible color and fading on 24 already reviewed photos.

The appearance pilot uses [Qwen3-VL-2B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct), revision `89644892e4d85e24eaac8bacfd4f463576704203`, as a separate annotation assistant; FashionSigLIP remains the retrieval backbone. The model card states Apache-2.0 and the repository is ungated. The pilot is remote/private, image-only, greedy generation, and receives neither product titles nor human similarity responses. It predicts observed color/tone/lightness, apparent fading and visible local details; hidden or unreadable attributes must remain unknown. Strict schema/consistency validation does not establish visual accuracy. No machine description is promoted to human ground truth, and schema validity alone is insufficient to justify retraining.


## Candidate-pool diagnosis after rejection

The selected audit searched only within the 39-image proxy validation fold (38 eligible candidates per selected query). A private CPU run reused the existing 372-image embedding cache and searched all cross-group images: 371 candidates per query, including training images. Both queries now have a different top-1 from the restricted audit, but the frozen and fit-adapted encoders choose the same expanded-gallery top-1. Their top-8 sets overlap 8/8 and 7/8. No additional model encoding or training was performed.

This is a development diagnosis of the candidate restriction, not held-out performance or evidence that an acceptable neighbor exists. The remaining 190 provisionally accepted images lack embeddings in this cache. Codex inspected the two expanded sheets without assigning human grades. Training-cut agreement and whole-appearance similarity remain different targets: do not expand fit-only training or the rejected VLM annotation pipeline on this basis. Establish credible whole-appearance positives and separate candidate availability from ranking before the next adaptation. [Execution evidence](verification/gallery_diagnosis_20261029.json).
