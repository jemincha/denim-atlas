# Sprint 1: machine-supervised regional pilot

2026-11-05. The researcher delegated axis judgments to the conversational visual
assistant. This replaces the pending manual annotation gate for this pilot;
machine judgments do not become human truth. Earlier human grades and quarantined
Qwen drafts remain unchanged. Sprint 1 is complete **as preparation for a small
distillation experiment**, not as matching-quality validation.

## Delivered inputs

- Cached source audit on private Kaggle CPU: 1,200/1,200 acquisition hashes and
  562/562 screened-observation hashes verified. Every audited image is228x298.
  Supplied metadata has no URL fields; a higher-resolution source was not recovered.
- 27 observations,54 source-derived garment/hip-thigh rectangles,10 anchor cases.
  Known source groups and decoded-pixel/file duplicates cannot cross the new
  train18/development9 folds. Existing reservation overlays remain excluded.
- 20 machine decisions, independently by silhouette/surface:18 strict preferences,
  one distance tie and one neither. The neither enters neither ranking loss nor
  negative grades;19 constraints remain. Strict training anchors: silhouette7,
  surface5; development3 per axis. Reused candidates/reciprocal cases are dependent.
- Actual byte checks, crop derivation checks and provenance/split validation passed
  on the private inputs. The engineering readiness threshold is3 strict training
  anchors and2 development anchors per axis; it does not establish sample adequacy.

[Aggregate counts and artifact hashes](verification/sprint1_machine_readiness_20261105.json).
Raw photographs, labels, reasons, groups and training inputs remain private.

## Label provenance and interpretation

The teacher was this **Codex conversation's multimodal visual assistant**, directly
inspecting the source and region boards. No separate ChatGPT API was invoked.
The interface did not expose a verifiable model checkpoint; do not attribute the
export to a named GPT API model. Frozen outputs and image/rubric hashes support
audit, but exact inference replay and repeat consistency are unestablished.

[Versioned axis rubric](../prompts/regional_axis_teacher_v1.txt) separates visible
volume/profile from color/lightness/cast and fade contrast/pattern/location.
Confidence is ordinal self-assessment. Neither and unknown never become zero
grades; ties constrain relative distances, not identity. No categorical attribute
labels or nDCG grades are inferred from these preferences.

The generic importer does not replace the legacy human-grade importer:

```sh
python scripts/regional_supervision.py --packet data/private/regional_sprint1_20261105/packet.json --ratings data/private/regional_sprint1_20261105/teacher_ratings.json --output runs/regional-training-input.json
```

Output creation is exclusive. It includes frozen decisions, safe constraints,
source/crop provenance and grouped folds. Readable broad cues support this small
trial; texture, subtle yellow cast and tiny distressing remain limited by pixels.

## Fixed comparison contract and next experiment

Sprint 2 keeps the pinned FashionSigLIP encoder and the planned E0/E1/E2 controls.
Use garment-wide evidence for silhouette, garment-wide plus corresponding
hip/thigh evidence for surface. Fit only on the train fold; inspect the development
fold separately. Preserve neither/U and report coverage; do not compute graded
nDCG from A/B labels. Development preference agreement measures teacher
reproduction, not human acceptance. Loss reduction alone is not a quality result.

For a later strong general-model comparison, freeze model identifier/version,
access route, prompt, image hashes, preprocessing and candidate pools before
scoring independent material. Give the comparator the same readable garment and
region evidence, no source names or adapted-model rankings. Return both axes
separately with uncertainty. Compare within-pool ordering separately from retrieval
coverage; report domain, per-query uncertainty and failures. Do not reuse this
teacher's training decisions as independent evaluation truth.

Exact strong-comparator execution access/version remains a later experiment gate;
the conversational labels do not resolve it. An API requiring payment still needs
authorization. A second independent evaluation route is required for a defensible
claim of superiority, even if manual training annotation is eliminated.
