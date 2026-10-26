# Denim Atlas — status, 2026-10-26

Small research study of visible denim similarity across different products. Compare observed color/tone, wash/fading and silhouette; no personal-taste objective, original-color reconstruction or app UI.

## Evidence

- Pinned Marqo-FashionSigLIP on Kaggle T4. First real-label fine-tuning completed: last vision block, 7,087,872 parameters, 40 steps, 222 clear-grade triplet combinations from 27 images. Training hinge loss 0.079425 → 0.018524; saved block-weight restoration verified. Private notebook version 362347502.
- 900 screening images audited. ABO 600 rejected as unsuitable; 24 clear GLAMI catalog crops selected. Commons wearing crops supply three pilot queries. The curated gallery is not representative of mixed-background inputs.
- One human rater completed 75 rank-blind trials. Two of three repeats matched; one 0/1 conflict is excluded. Usable labels: 71 unique pairs, no U responses. Three repeats do not establish rater reliability.
- Actual calibration nDCG@5, B0/B1: Q2 0.640659/0.639945; Q3 0.529635/0.446854. Q1 has an incomplete pool and no metric. Fixed color weight 0.5; no label-driven search.
- 39 local tests pass. Strict evaluation rejects split leakage and incomplete pools. Calibration scoring is separate from held-out evaluation.

## Limits and next gate

No held-out quality result, verified independent product groups or frozen research splits. The three pilot queries are now training data. Keep raw inputs/labels/weights private; publisher license metadata is not independent clearance for every image or a checkpoint release.

Paused at the researcher's request for folder organization. Next: expand permitted denim data and iterate fine-tuning, obtaining human labels when needed. Existing starting-model validation is finished. Additional GLAMI acquisition supports a disjoint ID window but has not been executed. Dataset access requests remain pending verification.

See [pilot protocol](docs/JUDGMENT_ROUND1.md), [evaluation](docs/EVALUATION.md) and [feedback audit](docs/FEEDBACK_AUDIT.md). Internal operational history is excluded from the current tracked state; prior commits retain their historical contents.
