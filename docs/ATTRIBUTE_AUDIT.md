# Attribute-label feasibility: first execution

October 29, 2026. Stage1 inventory and machine review completed; stage2 awaits six human attribute answers. No new training or model inference was performed.

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

The request, display mapping, original image hashes and sheet hash are private in `data/private/attribute_audit_20261029/`. Human answers received: **0**. Existing overall pair judgments are not converted into these attributes. No new annotation website or extra agreement is needed.

After the answers: record exact human observations, compare attributes independently, resolve the ordinal anchors, and decide which prompt/measurement needs revision. Passing this six-image check alone does not approve automatic annotation of all 562 images. Only expand a bounded weak-label pilot after its relevant gate passes, then assess broader error coverage before using those labels in training. Continue holding wash descriptions and preserve protected groups before any pair mining.

## Validation and reproduction

64 local tests passed, including coarse-field isolation, target ambiguity, conflicting title tags, missing/duplicate descriptions and image-provenance rejection. Rendering verified that all six numbers and garments are readable and no machine labels appear on the human sheet. These checks establish software behavior, not model quality.

The CLI accepts `--examples`, `--source-rows`, `--manifest`, `--descriptions` and a new `--output` directory. Raw inputs remain private and are recorded by SHA256. [Aggregate execution evidence](verification/attribute_audit_stage1_20261029.json) · [representation proposal](SIMILARITY_DESIGN.md).
