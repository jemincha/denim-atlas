# First real-label fine-tuning pilot — October 26, 2026

Marqo-FashionSigLIP is the fixed starting model. This is actual image-encoder fine-tuning, not a synthetic gradient check or a new standalone baseline-validation project.

The first run used the 27 reviewed crops and the researcher's existing judgments. Within each of three queries, grades 2/3 form closer candidates and grade 0 forms less-similar candidates; grade 1, uncertain judgments and conflicting repeats are excluded. This yields 222 triplet combinations from existing images, not 222 independent images. The same three calibration queries are now training data and cannot be called held-out test queries.

Only `visual.trunk.blocks.11` was trainable: 7,087,872 parameters. Fixed settings: 40 AdamW steps, learning rate 1e-5, weight decay 0.01, cosine hinge margin 0.1, seed 17, FP16 autocast/GradScaler, gradient clipping at 1.0. The existing evaluation preprocessing preserves observed color: no color jitter or random crop. Other model parameters stay frozen. Model evaluation mode disables stochastic layers but does not disable gradients in the selected block.

| Measured item | Result |
|---|---:|
| Mean hinge over all 222 training combinations, before | 0.0794250071 |
| Same training objective, after | 0.0185235348 |
| Optimizer steps | 40 |
| Checkpoint bytes | 85,076,277 |
| Trainable block changed | Confirmed by before/after checksums |
| Saved block weight restoration | Verified in the same kernel |

These are fitting results on the training observations. No unseen quality, population agreement, final checkpoint selection or interrupted-job determinism was tested. Product identities remain unresolved. The checkpoint contains the trained block and optimizer/scaler/RNG states; restoration verification covers block weights, not a complete interrupted training replay. Load the pinned base revision before applying the block state. Raw images, individual labels and weights remain private, with separate publication rights review required.

Run on Kaggle GPU with OpenCLIP 3.3.0 and the reviewed input directory:

```sh
python scripts/finetune_denim_pilot.py --input-root /path/to/reviewed-input --output /kaggle/working/new-training-output
```

Output must be new. `packet.json`, `ratings.json`, `manifest.json` and crops must match the reviewed packet. The script refuses local/CPU training and checks the base weights, crop hashes, finite gradients, parameter change and saved-weight restoration.

Actual result: [aggregate execution report](verification/denim_finetune_pilot_20261026.json). Private Kaggle notebook `jemincha/denim-atlas-denim-fine-tuning-pilot`, version **362347502**, preserves the source, triplets, report and block checkpoint. Additional source-data acquisition was prepared but not executed before the user requested a pause. Next work prioritizes expanding permitted data and iterative fine-tuning.
