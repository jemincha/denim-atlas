# Attribute-label feasibility: first execution

October 29, 2026. Stage1 inventory and machine review completed. Six human anchor answers are now recorded; a coarse-only retry is described below. No retrieval-model training has been performed.

## Existing evidence, separated by attribute

`prepare_attribute_audit.py` joins the 562 reviewed catalog candidates, their source titles, and the existing 24-image VLM pilot with image/checksum provenance. Three prior Commons crops bring the observation count to 565.

| Attribute | Available draft | Current decision |
|---|---|---|
| Retail fit | 375 explicit, unambiguous weak title tags | Preserve source terminology; do not equate it with observed volume/profile or overall relevance |
| Observed color family | 24 VLM drafts; blue16 / neutral8 after black/gray/white normalization | Small blind human calibration; no training-quality certification |
| Dominant lightness | 24 VLM drafts; medium20 / dark4 / light0 / unknown0 | Hold: qualitative inspection found white/pale/dark examples collapsed into medium |
| Observed tone | 24 VLM drafts; neutral15 / cool9 / warm0 | Hold until yellow-cast anchors and reference labels exist |
| Wash/fading details | Earlier pilot rejected | Excluded; coarse-field inspection does not rehabilitate local wash assertions |

The entire inventory is marked not training eligible and not human verified. Coarse fields are parsed independently from unrelated full-response wash/view failures, while preserving the original full-schema validity flag. Unknown and ambiguous targets stay unknown. No title word becomes a photographed-color label.

Codex inspected all 24 hash-verified photos. This is preliminary machine-assisted screening, not human ground truth or measured annotation accuracy. The previous pilot predictions were reused; only 21 already screened small catalog files were transferred from the private CPU asset-reuse job. No local weights or additional dataset acquisition.

## Six-image human gate

A blind image sheet requests only blue/near-neutral/other/U and dominant photographed lightness (dark/medium/light/mixed/U). No silhouette, tone, wash or similarity score is requested. The subset deliberately includes white, dark blue, lighter blue, black, gray and an existing wearing crop. It is a targeted anchor/failure probe, not a random accuracy sample. Images are reused development/calibration material, not a pristine test.

The request, display mapping, original image hashes and sheet hash are private in `data/private/attribute_audit_20261029/`. The original request is preserved unchanged; a separate response file records **six answers**. Existing overall pair judgments are not converted into these attributes. No new annotation website or extra agreement is needed.

Passing this six-image check alone does not approve automatic annotation of all 562 images. Only expand a bounded weak-label pilot after its relevant gate passes, then assess broader error coverage before using those labels in training. Continue holding wash descriptions and preserve protected groups before any pair mining.

## Human anchor result and coarse-only retry

The user supplied five explicit color-family values and six brightness values. “Raw denim” for image5 does not identify color or certify processing history; that color entry remains unassigned while its dark brightness is recorded. “Very light” for image6 remains verbatim and maps to the existing light bin without inventing an extra interval.

Against the original predictions, color-family agreement is **5/5 comparable**, brightness **2/6**. These selected development-anchor counts are not population accuracy. Original request, raw responses and predictions stay separate. No similarity grades or training eligibility were inferred. [Anchor comparison](verification/attribute_anchor_calibration_20261029.json).

The next bounded probe keeps the pinned Qwen model but uses `--coarse-only`: color family, dominant photographed lightness and target ambiguity only. It explicitly separates white/pale blue from deep navy/black and excludes background, fade strength and manufacturing inference. The six judged anchors are excluded from the 18-image manifest; those remaining photos are unjudged development observations, not an independent test with known ground truth. Schema/label-distribution changes alone cannot establish an accuracy improvement. No rejected wash output is reinstated.

Both bounded retries completed on T4 with unchanged pinned model weights:

| Inference context, same 18 targets | Dark / medium / light | Color family blue / neutral | Interpretation |
|---|---|---|---|
| Revised text instructions only | 6 / 12 / 0 | 13 / 5 | Pale examples still received medium in Codex visual inspection; do not scale |
| Same instructions plus five human-labeled reference images | 6 / 9 / 3 | 17 / 1 | Light labels appear, but four family predictions shift from neutral to blue; not an accuracy improvement claim |

The text-only run returned exact JSON code fences despite being asked for bare JSON; the original strict parser rejected all 18. Raw responses/statuses remain unchanged. A separate exact-fence normalization passes the same field/value/duplicate checks on 18/18, with no new inference. This repairs transport parsing, not visual quality. [Text-only execution](verification/coarse_attribute_retry_20261029.json).

Visual references are inference context, not gradient updates. The five anchors have explicit human values for both fields; image5 is excluded because its family was not supplied. Anchors and target IDs are disjoint. Full source-group independence is not asserted. [Reference-image execution](verification/coarse_visual_anchor_probe_20261029.json).

Keep the context variants separate. A private experimental fieldwise draft takes family from the text-only run and brightness from the reference-image run; this source choice was made on development inspection and is not validated or training eligible. No model self-confidence is used. Three deliberately selected unjudged photos now form the next blind human gate: pale appearance, a family-disagreement case, and a mid-level control. Only family and brightness are requested, with model predictions hidden. This still does not establish population accuracy or clear large-scale annotation/training.

## Validation and reproduction

68 local tests passed, including coarse-field isolation, the exact coarse-only schema, transport fences, verified/disjoint visual anchors, target ambiguity, conflicting title tags, missing/duplicate descriptions and image-provenance rejection. Both blind sheets were visually inspected. These checks establish software behavior, not model quality.

The CLI accepts `--examples`, `--source-rows`, `--manifest`, `--descriptions` and a new `--output` directory. Raw inputs remain private and are recorded by SHA256. [Aggregate execution evidence](verification/attribute_audit_stage1_20261029.json) · [representation proposal](SIMILARITY_DESIGN.md).
