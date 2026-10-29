# Silhouette and surface appearance: separation audit

October 29, 2026. This audit corrects the interpretation and collection protocol; it does not report a new trained model or retrieval gain.

## Finding

**The two axes were not adequately separated end to end.** Historical human sheets explicitly requested one joint visible-appearance grade. The latest proxy training optimized source-title cut agreement in a single shared image embedding. Neither provides independently measured silhouette and surface similarity.

The researcher clarified that either a large silhouette difference or a large color/surface difference was enough to reject a pair. Those answers are valid under the joint prompt. They do not imply that both axes were poor, that the researcher misunderstood the task, or that an existing overall grade can be split retrospectively. Preserve all original labels and packet hashes.

| Stage inspected | Actual implementation before this correction | Consequence |
|---|---|---|
| Human rounds 1–3 | `judgment_template.html` asked for color, wash and silhouette together; `import_judgments.py` returned one `grade` | Overall rejection is interpretable; the failed axis is unknown |
| Human-label continuation | `training_triplets()` used overall grade >=2 versus grade0 | Joint supervision, not two independent attribute objectives |
| Source-cut proxy | `batch_triplet_loss()` used same `source_fit` as positive, different cut as negative, with no surface constraint | Different colors/washes can be pulled together, and surface-similar different cuts pushed apart. Whether/how much this caused observed failures is unmeasured |
| Proxy evaluation | `proxy_metrics()` used equality of title-cut classes as relevance | Reported gains measure weak cut-class agreement, not full observed silhouette geometry or surface quality |
| Retrieval and candidate selection | One FashionSigLIP embedding/cosine per image; selected audit searched 39 validation images | No axis-conditioned distances; title class, viewpoint and candidate coverage can confound interpretation |
| Surface work | B1 uses mean RGB; VLM appearance pilot was not accepted for training | RGB is not a wash/texture metric. There is no validated surface-supervised model |

In the two rejected spot-audit rows, private source-cut labels were `(skinny, skinny, skinny)` and `(straight, wide, straight)` for reference/A/B. These are weak title labels, not human geometry judgments. The first row alone illustrates why source-cut agreement cannot certify overall resemblance; it does not prove surface is the only cause.

## Operational targets

| Axis | Compare | Exclude from that axis |
|---|---|---|
| `silhouette` | Visible leg outline, relative thigh/knee/hem widths, taper/flare and observed looseness | Color, wash, fading and rips as style details. Do not infer hidden garment shape from a product name |
| `surface` | Observed lightness/color/tone, readable texture, apparent wash/fading strength and placement, visible whiskers and rips | Fit category and leg width. Do not restore presumed original color or infer a manufacturing/wear process |

For each axis: 0 = almost no resemblance; 1 = partial overlap with large differences; 2 = close with noticeable differences; 3 = very close. `U` means that axis cannot be read reliably. Occlusion, view and resolution affect observability separately: silhouette U / surface2 is a valid record. Uncertain texture or a hidden fading region must not be invented. The surface axis still groups several attributes; disagreement within that axis is a remaining rubric-calibration issue.

Same fit / different surface and different fit / similar surface are useful diagnostic contrasts, not automatically bad pairs for every objective. Neither source titles, model proximity nor Codex screening assign the human axis grades. Candidate mining must retain those contrasts and document the selection; it must not require both axes to match before collecting axis-specific evidence.

## Implemented correction

- New packet CLI output defaults to schema2 with `comparison_axes: [silhouette, surface]`. One pair is shown once with two independent score groups and separate uncertainty reasons; no extra overall score is required.
- Export/import preserves `scores.silhouette` and `scores.surface`. Partial answers, U, repeat agreement and conflicts are processed per axis. A conflict on one axis does not discard the other. No joint grade or automatic mean/minimum is produced.
- `analyze_calibration.py` requires an explicit axis for schema2 and reports that axis in its output. A historical overall grade cannot be requested as a silhouette/surface grade. Reusing one embedding for these descriptive scores does not make it an axis-specific model.
- The existing joint-grade fine-tuning entry point explicitly rejects schema2 instead of silently generating training triplets from mixed axes.
- Historical schema1 import and packet construction remain available. `packet()` retains its legacy default for existing programmatic callers; new callers must pass `separate_axes=True`. CLI `--legacy-overall` reproduces the old format. Existing private packets are not rewritten.

Example for a **future reviewed calibration packet**, not a request for another large rating round:

```sh
python scripts/build_judgment_packet.py --queries queries.json --gallery gallery.json --pools pools.json --packet-id denim-atlas-axis-pilot-v1 --output data/private/axis-pilot
python scripts/import_judgments.py --packet data/private/axis-pilot/packet.json --ratings ratings.json --output imported.json
python scripts/analyze_calibration.py --packet data/private/axis-pilot/packet.json --ratings ratings.json --features features.json --comparison-axis silhouette --output silhouette-report.json
python scripts/analyze_calibration.py --packet data/private/axis-pilot/packet.json --ratings ratings.json --features features.json --comparison-axis surface --output surface-report.json
```

These analysis commands retain the frozen-feature provenance checks and complete-pool requirements; they do not launch another starting-model validation. Inputs need actual reviewed assets/ratings. Calibration records do not become a group-verified benchmark automatically.

## Next training decision and limits

The [working representation and similarity design](SIMILARITY_DESIGN.md) expands each axis into subordinate attributes, separates volume from leg profile and color family from lightness, and proposes a calibration policy. It is not a frozen ontology or an implemented scoring model.

Do not continue the fit-only objective as evidence of whole-appearance progress. First obtain credible, observable axis-specific supervision on a small diagnostic contrast set, using existing assets and requesting human input only for unresolved cases. No new human labels have been produced by this software change.

Then retain the pretrained backbone and use explicit axis-conditioned distances/objectives, such as two small projection heads. That model change is **proposed, not implemented or validated**. Source-cut labels remain a weak silhouette proxy. Surface supervision and protected product groups remain unresolved. Independently report each axis, plus joint acceptability only if directly judged under a defined rule; do not hide a failed axis by averaging it with the other. Thresholds, weights and checkpoint selection must be fixed on development data before a fresh test.

Software verification covers disagreeing axis values, one-axis unknown/missing labels, per-axis repeat conflicts, provenance, prohibited pooling, legacy behavior and explicit-axis metrics. A private engineering browser preview checks controls, persistence, actual JSON download/import and mobile layout; its test clicks are synthetic fixtures, never researcher labels. [Verification record](verification/axis_separation_audit_20261029.json).
