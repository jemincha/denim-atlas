# Denim Atlas: visible denim appearance similarity

A small research study adapting a pretrained vision encoder to retrieve similar-looking denim across different products. Compare current photographed color, tone, fading, wash patterns and silhouette, including lighting effects. Do not reconstruct original fabric color or learn the author's personal taste. Mobile apps and shopping integration are outside this study.

**Status:** Kaggle T4 inference and synthetic backward/checkpoint checks passed. A Fashionpedia metadata audit produced 314 pants candidates, including 109 source `jeans` labels. No real denim training or held-out retrieval improvement has been demonstrated.

## Compute and model

- Model: `Marqo/marqo-fashionSigLIP`, OpenCLIP 3.3.0, 224-pixel input, 768-dimensional embeddings.
- Saved execution resolved revision `c56244cc94f92419e8369fa71efdaf403b124ce8`; checksum and exact environment are in `docs/verification/model_check_20261023.json`.
- Generic SigLIP comparator is planned but has not run.
- The old laptop is for editing and small tests. Download weights, process image collections and train on remote free compute.
- In one remote GPU kernel, run `scripts/check_remote_gpu.py`, then `scripts/check_remote_model.py`, then `scripts/check_remote_backward.py`. The latter two share kernel variables. Synthetic checks are not a training recipe or quality evaluation.
- `scripts/inspect_fashionpedia.py` runs a metadata-only audit on Kaggle CPU. Source image rights and product identities remain unverified.

## Experiment requirements

1. Acquire usable images and record provenance, rights, crops and product/duplicate groups.
2. Split by product group before constructing training pairs. Do not equate same product with visible similarity or different products with dissimilarity.
3. Freeze human-judged cross-product candidate pools with grades 0–3; keep uncertain and unobservable cases explicit.
4. Compare frozen Marqo, frozen Marqo plus color reranking, and a fine-tuned copy of the same starting checkpoint.
5. Report held-out nDCG@5, per-query errors, uncertainty, settings and limitations. Tune on validation only.

Recovered notebooks were reconstructed from rendered saved code cells. Their local execution counts and outputs are intentionally empty. Actual observed results are in `docs/verification/`.

See [project state](PROJECT_STATE.md) and [recovery provenance](docs/RECOVERY.md).
