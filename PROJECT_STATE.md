# Denim Atlas — 2026-10-29

Goal: retrieve different denim products matching observed color/tone, wash/fading and silhouette. No personal-taste objective or app UI.

## Evidence

- GLAMI: 1,200 acquired images; 512 visually reviewed by Codex, 347 whitelisted. Low-resolution blue/gray studio bias.
- Weak-text adaptation: 347 images / 44 steps. Human continuation: 51 round-2 pairs, 71 triplet combinations / 142 FP32 steps. Training-pool nDCG@5 0.4493 → 0.8526; checkpoint restoration verified.
- New-query round completed: 54 trials / 51 unique pairs, three consistent repeats, no missing/uncertain responses. Grades 0:37, 1:9, 2:4, 3:1.
- Frozen weak-text versus human-continuation new-query nDCG@5 **0.3841 → 0.3513**; grade >=2 precision@5 0.2000 → 0.1333. Three query photos, same training gallery. No demonstrated generalization improvement.
- 46 local tests pass. Weights/bulk images stay remote; raw ratings/images stay private.

## Next work

No human-input gate or pending GPU training. The researcher reported that obviously dissimilar candidates waste labeling effort. Stop full cross-query rating grids; query-specific pools are now supported and tested. Retrospective count: 23 rather than 54 trials, but 13/20 corresponding model-selected pairs were still zero. Two positives were found only in the wider pool; filtering needs a coverage audit.

Prioritize data/appearance coverage, image suitability and candidate mining before requesting small batches of plausible/uncertain pairs. Machine attributes are weak supervision, not human grades. Keep frozen evaluation candidates separate from training-label mining; never hide bad retrievals from scoring. Existing new-query labels remain outside further fitting.

Product/duplicate groups and independent splits remain unresolved. Seller-image and checkpoint publication rights are not established. No access-request check this sprint.

[Protocol, results and revised workflow](docs/HUMAN_ROUND2.md) · [Result evidence](docs/verification/new_query_round3_results_20261029.json)

Methodology review completed: [primary-source benchmark and proposed sprint](docs/METHODOLOGY_BENCHMARK.md). The nearest reference is attribute-specific similarity learning. Audit available supervision before changing the architecture or requesting another rating batch; the detailed sprint is a proposal, not an executed experiment.
