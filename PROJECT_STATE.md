# Denim Atlas — 2026-10-29

Research target: retrieve different denim products matching observed color/tone, wash/fading and silhouette. No personal-taste objective, color restoration or app UI.

## Evidence

- GLAMI: 1,200 acquired images; 512 visually inspected by Codex, 347 whitelisted. Low-resolution blue/gray studio bias; source archive checksum verified.
- Weak-text adaptation: 347 images, 44 steps, loss 0.865115 → 0.823334. Old queries' top-5 initially unchanged.
- Round-2 human export: 54 trials / 51 unique pairs; three repeats consistent. Old labels not merged.
- Continued last vision block from the weak-text checkpoint: 71 triplet combinations, 142 FP32 steps. Training-pool mean nDCG@5 **0.4493 → 0.8526**; hinge 0.06014 → 0. Checkpoint restoration verified. These are training fitting figures.
- Retrieval review completed: all three training and all three new query top-5 rankings changed. New-query relevance remains unjudged.
- 44 local tests pass. Model weights and bulk data stay remote; official Kaggle CLI works.

## Current human-input gate

New packet `denim-atlas-new-query-round3-v1`: 3 different Commons wearing-photo crops × 17 candidates + 3 repeats = 54 trials. Private directory `data/private/judgment_round3/packet/`; localhost port 8879. Original round-2 export preserved. Await researcher JSON; do not assign grades.

On receipt: import with provenance checks, handle repeat conflicts/uncertainty, then compare the frozen weak-text and human-continuation rankings on the fully judged fixed pool before further fitting. Packet and checkpoint hashes are in the linked evidence. No pending GPU run.

New queries were not trained on, but the 347-image gallery was used for weak adaptation. Product/duplicate groups and independent splits remain unresolved. Rank changes alone are not improved quality. Raw images, ratings and weights remain private; publication rights for seller images/derived weights are unresolved. Access-request status was not checked this sprint.

[Protocol and evidence](docs/HUMAN_ROUND2.md) · [Research design](docs/RESEARCH.md)
