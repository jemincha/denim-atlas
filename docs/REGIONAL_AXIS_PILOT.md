# Sprint 2: regional, axis-specific adaptation

2026-11-05. **Completed experiment; no development preference-agreement gain.**
This is machine-teacher distillation on selected development material, not evidence
of human matching quality or superiority to a strong general multimodal model.

## Fixed experiment

Reused Sprint1's27 observations and54 source-derived garment/hip-thigh views.
Train18/development9 source groups remain separate. Training uses13 constraints:
silhouette7 strict, surface5 strict plus1 distance tie. Development has3 strict
preferences per axis, sharing3 anchors. Neither/U do not enter either loss.

The pinned FashionSigLIP encoder stayed frozen. White aspect-preserving padding
precedes its transform; observed colors remain unchanged. E0 uses garment-wide
features; E1 adds equally normalized garment+hip/thigh features for surface.
Silhouette uses garment-wide features in both. E2 adds separate bias-free linear
64-D projections:768->64 silhouette,1536->64 surface;147,456 trainable parameters.
The untrained E2 initialization is also reported to expose random-projection effects.

One configuration was fixed before execution: seed37,200 full-batch AdamW steps,
lr0.0003,weight_decay0.01,cosine margin0.05. Strict preferences use ranking hinge;
ties use absolute difference between two similarities. The two axis losses receive
equal weight. No development decisions enter the loss or checkpoint selection.
No sweep, last-block unfreezing or post-result checkpoint selection occurred.

## Results

Counts below are **agreement with the frozen machine preferences**. They are not
absolute relevance grades and cannot be converted to nDCG.

| Experiment | Train silhouette | Train surface, strict only | Development silhouette | Development surface |
|---|---|---|---|---|
| E0 garment only |2/7|3/5|2/3|2/3|
| E1 garment+region |2/7|1/5|2/3|2/3|
| E2 untrained projection |1/7|1/5|1/3|2/3|
| E2 trained projection |7/7|5/5|2/3|2/3|

The trained surface head also satisfies the one training tie. Equal-axis training
loss fell0.066095->0.00006586. This establishes fitting, not improved matching.
Development silhouette fixes one preference but regresses another; mean signed
margin versus E1 worsens0.004686->-0.015006. Surface fixes none; its mean signed
margin improves0.001442->0.008630 without changing any winner. Tiny selected samples
do not support significance claims or a causal diagnosis of overfitting.

## Failure analysis and next decision

- The silhouette regression occurs in a near-black, straight/width comparison;
  training makes the previously correct choice strongly disagree with the teacher.
  The fixed silhouette case is a tapered-versus-wide contrast. A net2/3 hides this
  exchange; retaining only the improved example would misrepresent the result.
- The surface disagreement persists on a pale grey-blue tapered reference versus
  darker patterned and paler uniform alternatives. The trained distance is closer
  to a tie but still chooses the teacher-disfavored option. This is disagreement
  with this teacher, not independently established human error.
- All3 development cases have the same preferred candidate on both axes; all9
  development photographs are isolated catalog views. This set cannot establish
  generalized axis decoupling or wearing-to-catalog robustness.
-13 dependent constraints versus147,456 parameters are severely underdetermined.
  The fitting/development gap is compatible with overfitting. It does not establish
  whether labels, representation, crop alignment or capacity is the dominant cause.
- All sources are228x298. No training can establish fine texture absent from the
  pixels; a larger model is not the next justified move.

Next controlled investigation: strengthen frozen development coverage with
axis-conflicting alternatives and wearing views, preserving group reservations and
machine-label provenance. Separately compare a lower-capacity adaptation on the
same features/labels before unfreezing the backbone. Keep these changes separate;
new data and reduced capacity together would obscure what helped. Do not declare
these teacher labels an independent strong-model benchmark or ask for another
manual training grid by default.

## Execution and verification

Private Kaggle kernel `jemincha/denim-atlas-regional-axis-pilot`,version2,completed on
TeslaT4. Encoder download/loading/feature extraction took44.70s; that plus head
training and saving took46.71s. Queue, environment setup and failed transport time
are excluded. The initial oversized request returned400; after separating private
data, runtime1 exposed Kaggle's ZIP auto-extraction. Runtime2 fixes input discovery;
learning settings, source bytes and labels were unchanged.

84 local tests passed before execution. Actual run verified input/model/crop
provenance, finite updated parameters, no development-score gradient in the loss,
and exact prediction restoration from the saved checkpoint. Independent local
standard-library recomputation of E0/E1 outcomes agrees with GPU output; maximum
similarity/loss difference1.83e-7. Weights stayed private on Kaggle; only feature
JSON, results and logs were downloaded. No paid API call or new human labels.

```sh
python scripts/regional_experiment.py --inputs /kaggle/input/PRIVATE_DATASET/inputs --output /kaggle/working/regional_experiment
```

Use the directory containing the frozen packet/ratings and assets; outputs must be
new. Requires the existing remote CUDA environment and `open_clip_torch==3.3.0`.
Raw input and model weights are not distributed by this repository.

[Preflight/config](verification/sprint2_preflight_20261105.json) ·
[Aggregate results/provenance](verification/sprint2_results_20261105.json) ·
[Execution checks](verification/sprint2_checks_20261105.json) ·
[Sprint review](SPRINT_REVIEW.md).
