# Observed-appearance annotation feasibility — October 29, 2026

The researcher rejected both recommendations in each of two selected comparisons. These are recorded as **neither / neither**, with no absolute grades, tied preferences or training triplets inferred. Rejection reasons were not supplied. This motivates testing whether reusable surface descriptions are available; it does not establish which facet caused rejection. [Feedback record](verification/glami_fit_spot_audit_results_20261029.json).

## Public annotation taxonomy audit

A remote CPU job inspected the official [Fashionpedia validation annotations](https://github.com/cvdfoundation/fashionpedia#annotations). The 14,533,475-byte JSON contains 294 attributes and 314 pants instances. Matching terms were `jeans` (109 pants instances), `washed` (68) and `distressed` (21). These counts overlap; washed/distressed counts are over all pants, not confirmed denim. This taxonomy did not supply explicit photographed color/tone or fine fading strength/location targets for our task. Absent attribute IDs are not automatically negatives. No images were downloaded and no image permissions or training-ready denim were inferred. [Taxonomy evidence](verification/surface_attribute_taxonomy_20261029.json).

## Pinned image-only description pilot

[Qwen3-VL-2B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct) was used only as an annotation assistant, not as a replacement retrieval model. Official metadata reported an ungated Apache-2.0 model. Revision `89644892e4d85e24eaac8bacfd4f463576704203` and actual safetensors SHA-256 are recorded; the script now checks that weight hash explicitly. Code uses built-in Transformers classes with remote code disabled.

The 24-image pilot consists of six assets from the rejected comparisons, 15 seeded cut-diverse catalog images and three existing Commons query crops. All images had previous private-research review and byte hashes. The model received pixels and a fixed prompt; no source titles, cut labels or human answers. Observed lighting is retained, original material color/wear is not reconstructed, and no manufacturing process or overall relevance is inferred.

Greedy FP16 inference ran on Kaggle T4 with Transformers 5.16.1 and SDPA; no paid inference API or laptop weights. Inference for 24 images took 108.81 seconds after loading, peak allocated memory 4.078 GiB. The source model snapshot remained remote. No retrieval model was trained or reranked.

## Outcome: do not scale these labels

The original exact-schema/consistency parser accepted **22/24** responses; two outputs violated the requested back/side front-detail masking rule. Among the initially accepted responses, **21/22** asserted visible front-hip whiskers; none used unknown for any visual enum and all called detail readable enough. Fading strengths collapsed to moderate (18) or none (4). These distributions alone do not measure accuracy, but are warning signals given varied materials, views, contrast and limited resolution.

Visual inspection of the six already displayed audit assets and existing query crops exposed implausibly repetitive local-detail descriptions. A post-review rule rejects `fade_strength=none` together with explicitly faded hip whiskers; three further responses violated that contract. **19/24** passed the revised consistency check. This is a post-hoc safety check, not a new model run, accuracy score or a tuned research performance metric. All raw outputs and original validity statuses are preserved privately. The executed script/prompt hashes and revised validator hash remain separate.

The masking rule itself is imperfect: an oblique front view can reveal front details even if tagged side, so a rejection can arise from the view label/schema. Thigh/knee brightness can come from lighting; it is allowed with no fading and is not automatically treated as an irreversible wear effect. No human attribute-accuracy ground truth was collected.

**Decision:** do not automatically annotate all 562 images or train on these descriptions. Coarse color may help generate proposals, but fine wash features and unknown handling need independent review. Schema-compliant output is not a training-quality label. [Machine pilot evidence](verification/appearance_annotation_pilot_20261029.json).

## Implementation and next gate

`annotate_denim_appearance.py` is bounded to 1–24 previously reviewed, hash-pinned images on remote CUDA. It rejects duplicate JSON keys, missing/extra fields, invalid enums, unobserved/unreadable detail assertions and inconsistent ambiguity. Raw response text, unknowns and errors remain explicit; there is no automatic conversion to negatives, numerical confidence or relevance grades. Tests run without downloading the model locally.

The next requested human input is a short description of the largest concrete mismatch in each of the two already shown comparisons. This is an error diagnosis, not a preference-weight interview or another rating grid. Use the response to define/check an observable target before another annotation or training experiment. Existing fit-only checkpoints remain experimental; the 39-image proxy validation improvement does not establish overall matching quality.

No pending compute jobs, new image agreement, raw-image publication or model-artifact release. Primary source cards/licenses do not independently clear upstream seller images.
