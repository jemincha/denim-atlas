# Denim Atlas — current state (2026-10-23)

- Goal: a small reproducible fine-tuning study of cross-product visible denim similarity. No personal-taste objective or mobile UI.
- DeepFashion2: user reports the application was submitted. No related mail found in the connected application-email Gmail account at the latest check. Do not re-submit, contact maintainers or infer access approval without evidence.
- Runtime: Kaggle T4 x2, 14.562GiB per device. Marqo batch 2 produced 768-D embeddings. Synthetic full-vision AdamW update and same-kernel checkpoint restoration passed; measured peak allocated VRAM 2.166GiB. Not denim learning or interrupted-job reproducibility.
- Fashionpedia: metadata-only audit, 314 pants instances / 313 images, 109 source jeans labels; no confirmed denim, verified product groups or research splits. No source images downloaded.
- Local project folder was observed empty, including its previous .git, in ordinary and unsandboxed read-only checks. Cause unknown. Do not describe a sync or deletion cause as established.
- Recovered from saved Kaggle rendered code: four Python scripts, two reconstructed notebooks and four exact parsed JSON reports. This is a partial recovery. Previous evaluator, tests, original planning documents and legacy PoC have not been recovered.
- Next: prepare/test annotation import while waiting for dataset access, then inspect real trousers/jeans, crop and group before constructing judgment pools. Model execution stays remote.
- Prepared scripts/prepare_deepfashion2.py and docs/NEXT_DATA_RUN.md. Five local fixture tests pass; no actual DeepFashion2 annotations have been processed. Source pair/style grouping is conservative screening metadata, not appearance relevance or verified identity.
- Dataset-access mail is still unverified; a Kaggle notification is not evidence of dataset approval.
- GitHub destination: https://github.com/jemincha/denim-atlas (private, as requested). Its remote commit history is the authoritative publication record. No dataset-maintainer contact has been sent.
- README now documents the original concept, scope decisions, research design, model acquisition, measured checks, data limits, reproducibility and remaining milestones.
- No private images, weights, passwords, personal addresses or signatures belong in Git.
