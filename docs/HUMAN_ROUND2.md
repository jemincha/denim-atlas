# Human relevance continuation — October 28, 2026

The researcher completed 54 rank-blind trials: 51 unique image pairs, plus three exactly consistent repeats. No missing or uncertain responses remained. Grades were 0:32, 1:12, 2:6, 3:1. Three repeats are a local consistency check, not population reliability. The duplicate downloaded exports contained identical judgments.

Two candidate source images also occurred in round 1. Four of six comparable source-level pairs received different grades across rounds, with different image views/preprocessing and a clarified rubric; these are not repeated identical trials. Old labels were not merged. See [import audit](verification/human_round2_import_20261028.json).

## Fixed continuation

Start from the completed 347-image weak-text checkpoint, not the earlier 27-image human pilot. Verify the pinned base revision, parent checkpoint SHA-256 and loaded block digest before training. Use only round-2 labels: positive grade >=2, negative grade 0; grade 1 contributes to descriptive ranking scores but not triplet construction. This yields 71 combinations (40 / 18 / 13 by query).

Fine-tune the last vision block in FP32 for 142 steps, two passes through the same seed-17 shuffled combinations, with a fresh AdamW optimizer, learning rate 1e-5, weight decay 0.01, cosine margin 0.1 and gradient cap 1.0. Preserve color with white letterboxing; no random crop or color jitter. All three queries are training data. The optimizer is deliberately fresh; this is block-weight continuation, not exact interrupted-job resumption.

## Completed run

Private Kaggle job `jemincha/denim-atlas-human-round2-fine-tuning`, version 1, completed on Tesla T4. It used 20 images (3 queries and 17 candidates), updated 7,087,872 parameters and saved an 85,076,085-byte block/optimizer checkpoint. Same-kernel block restoration passed. The measured training/report segment took 7.39 seconds with 0.883 GiB peak allocated memory; this excludes startup, model download and initial metric calculation.

| Training query | Fixed 17-candidate nDCG@5 before | After |
|---|---:|---:|
| Q1 | 0.7564 | 0.8777 |
| Q2 | 0.2626 | 0.9377 |
| Q3 | 0.3288 | 0.7425 |
| Macro mean | **0.4493** | **0.8526** |

Mean hinge over all 71 training triplets fell **0.0601407 → 0**. These figures establish that the selected block can fit the supplied relevance constraints. They do not establish retrieval improvement on new images or products. They are conditional on this fully judged 17-candidate pool, not nDCG over the entire 347-image gallery. The nDCG gain is the existing `2^grade - 1` definition.

[Aggregate training report](verification/human_round2_finetune_20261028.json) pins input hashes, code hash, parent/output checkpoints and per-query scores. Raw ratings, pictures and weights remain private.

## Next check fixed before new judgments

Compare the weak-text parent and human-continuation checkpoints on the same 347-image gallery. First inspect rank changes for the training queries, then prepare rank-blind pairs for three different, previously acquired Commons wearing-photo crops. Freeze checkpoints, query crops and candidate selection before receiving new labels; do not tune on those labels before reporting the comparison.

The new crops include a back waist/thigh partial view, a light distressed front view clipped below the knees, and a leaning gray/light denim view. They are deliberately different observations; obscured silhouette can be marked uncertain. Recorded CC0 / CC BY 2.0 attribution accompanies private review material. This is a new-query exploratory check on a training gallery, not a product-disjoint test. Product/duplicate groups remain unresolved and the sample is too small for a general quality claim.

Use the union of both checkpoints' top-5 candidates, hide model names and ranks during pair grading, and retain a separated repeat per query. Freeze the packet hash and save the researcher's export through the existing provenance-checking importer. No machine-assigned relevance grades.

## Retrieval inspection and pending new-query labels — October 29

Private job `jemincha/denim-atlas-human-round2-retrieval-review`, version 2, completed. Top-5 ordering changed for all three training queries and all three new query crops. The training-query lists shared 2 / 1 / 2 candidates before/after; the new-query lists shared 3 / 4 / 3. This is evidence of changed retrieval, not improved relevance. [Aggregate rank-change record](verification/human_round2_retrieval_20261029.json).

The union of top-5 candidates from both frozen checkpoints over the three new queries contained 17 unique images. All 3×17 pairs are presented in a randomized, rank-blind packet with one separated repeat per query: **54 trials**. The packet has no Codex relevance grades and no prior training-query source overlap. It keeps the same 0–3 / uncertain rubric, marks partial observations and includes attribution. The original round-2 export and browser draft are preserved separately.

Packet `denim-atlas-new-query-round3-v1` is hashed before labels; [preparation evidence](verification/new_query_round3_preparation_20261029.json) records crop, packet and HTML hashes. Private location: `data/private/judgment_round3/packet/`. Serve on localhost port 8879; round-2 uses port 8878. The HTML response was verified byte-for-byte over HTTP; the new sheet's browser interactions were not separately automated in this run. It reuses the tested judgment template.

After receiving the researcher's export, validate provenance, repeats, uncertainty and pool completeness. Compute both frozen rankings against the same completely judged 17-candidate pool before any new training. Do not score unjudged gallery images as zero. Preserve these observations as exploratory new-query evidence; product-disjoint generalization is still untested.

Version 1 of the retrieval-only job stopped before model comparison because its launcher looked for the wrong acquisition filename. Version 2 uses the verified `screening_images.jsonl`; checkpoints and candidate-selection rules were unchanged. No repeated training or label-driven checkpoint selection occurred.
