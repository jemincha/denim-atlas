# GLAMI expansion and weak text adaptation — 2026-10-26

This experiment uses existing product descriptions as weak image/text supervision, not invented human appearance grades. It is separate from the earlier 27-image real-label triplet pilot. Neither experiment establishes unseen-product retrieval improvement.

## Acquisition and visual gate

The official default-resolution archive was downloaded once on Kaggle CPU at publisher revision `befda45d8d4e8b8082bb8a1912d1f9eb9483991c`. Publisher MD5 `500348bbf54595db81cba353acd50d78` was verified before ZIP access. The archive stayed in temporary remote storage; only selected files were extracted. The acquisition script took approximately 126 seconds including metadata and sample sheets, not a general throughput guarantee.

The existing pants-category plus jeans/denim-text screen found 7,276 source records. The first 1,200 unique sorted image IDs were extracted and image-file verified: 12,434,870 image bytes. This includes the earlier first 300; it is not 1,200 additional images. The full source ZIP is not retained as a notebook output. Source train/test labels are not research splits.

An initial 96-image sample exposed non-denim/ambiguous pants from description matching. Requiring jeans/denim in product names left 1,012 unique acquired candidates. From those, 512 were sampled with seed 17 and individually inspected on eight contact sheets by Codex. The whitelist contains 347 IDs; 165 were excluded or uncertain. Seams, pockets, denim-like texture and visible fading informed screening, not personal taste. This does not certify physical fabric composition.

Several smooth, colored, white, coated or otherwise ambiguous examples, folded/multiple-garment/close-up-only views were excluded. Blue/gray catalog imagery is consequently overrepresented. Studio wearing photos are included; the corpus does not represent arbitrary lifestyle backgrounds. Default images around 228×298 cannot support claims about fine wash detail.

## Protocol fixed before results

- Start from the pinned Marqo-FashionSigLIP checkpoint already used by the project; verify original weight SHA-256.
- Use only visual-whitelist IDs. Verify acquired hashes and dimensions; deduplicate known item IDs, identical decoded pixels and normalized descriptions. Near-duplicate/independent-product certification remains unresolved.
- Freeze text encoding and all image layers except the last visual transformer block. Source name/description prefixes may be multilingual/noisy; they are not appearance-relevance labels.
- Use OpenCLIP 3.3.0's existing `ClipLoss` with frozen text embeddings and FP32 CUDA arithmetic. Batch 16, two epochs, seed 17, AdamW learning rate 1e-6, weight decay 0.01, gradient norm cap 1.0. Freeze original logit scale and cap at 100.
- Preserve the visible garment with a white letterbox before model preprocessing. No random cropping, color jitter or lighting restoration.
- Save block/optimizer, exact examples, whitelist, settings and step history. Verify block-weight restoration in the same kernel; interrupted-job reproducibility is not tested.

Compare loss before/after on identical fixed training batches. Do not interpret fitting as human similarity quality, product-disjoint validation or generalization. Different images/descriptions can be visually similar; in-batch negatives are a limitation of this weak text objective.

## Execution and reproduction

Private Kaggle jobs: `jemincha/denim-atlas-glami-bulk-screening` version 1 (acquisition), `jemincha/denim-atlas-glami-visual-screening` version 1 (review sheets), and `jemincha/denim-atlas-glami-text-fine-tuning` (GPU adaptation). The first two completed. Training results are recorded separately; submission alone is not completed learning.

GPU version 3 completed: all 347 visually approved examples remained after known-item/pixel/caption deduplication. Two epochs produced 44 optimizer steps; fixed-batch training loss decreased from **0.8651152284 to 0.8233336391**. The 85,070,133-byte block/optimizer checkpoint passed same-kernel block-weight restoration. Training-loop time was 14.53 seconds with 1.047 GiB peak allocated GPU memory on Tesla T4; this excludes setup/download/initial loss measurement and is not end-to-end runtime. Exact repository and executed training-script SHA-256 values matched. See [aggregate training evidence](verification/glami_text_finetune_20261027.json).

GPU version 1 stopped because the local model snapshot omitted tokenizer assets. Version 2 included tokenizer assets at the same pinned revision, then stopped on nonfinite FP16 gradients. Version 3 uses FP32, retains finite-loss/gradient guards and leaves the dataset, objective and optimization hyperparameters unchanged. The numerical repair is not a label-driven hyperparameter search. Neither failed attempt produced a completed checkpoint/report.

The qualitative A/B comparison completed in private job `jemincha/denim-atlas-glami-adaptation-ab`, version 1. All three existing Commons queries had exactly the same ranked top-5 candidate IDs before/after adaptation on the same 347-image training gallery. There is no demonstrated retrieval improvement from this run. These are previously used calibration queries, not an independent test. See [rank-stability evidence](verification/glami_retrieval_diagnostic_20261027.json).

Instead of asking for preferences between identical lists, a second rank-blind image-pair judgment packet was prepared. It uses the union of 13 retrieved candidates plus four random ungraded gallery examples (seed 23): 3 queries × 17 candidates plus 3 repeats = 54 trials. No grades were assigned by Codex. The 0/1 boundary is clarified and exports are separated by round ID with a provenance regression test. The actual browser sheet loaded at 0/54 and next/previous navigation was checked. See [packet evidence](verification/judgment_round2_preparation_20261027.json). The sprint is paused at the researcher's request; local serving stopped and private files remain for resumption.

`scripts/acquire_glami.py --bulk --max-images 1200 --revision befda45d8d4e8b8082bb8a1912d1f9eb9483991c` runs on Kaggle CPU. `scripts/finetune_glami_text.py` accepts an acquisition directory, exact-summary-pinned visual whitelist and new output directory on Kaggle GPU. It refuses unreviewed IDs and local/CPU training. An authorized account can retrieve exact private job source/metadata with `kaggle kernels pull <job> --metadata`.

Raw images, detailed source records, whitelist and weights stay private. Publisher license metadata is not independent clearance for every upstream seller image or for release of a derived checkpoint.

Sources: [official GLAMI download/checksum](https://github.com/glami/glami-1m#how-to-download-glami-1m-manually), [OpenCLIP loss](https://github.com/mlfoundations/open_clip/blob/v3.3.0/src/open_clip/loss.py), [Kaggle CLI](https://github.com/Kaggle/kaggle-cli).
