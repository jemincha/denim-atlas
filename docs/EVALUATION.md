# Fixed-pool evaluation

Implemented October 24, 2026. This is evaluation infrastructure, not a measured retrieval result. It uses only Python's standard library and can run locally without a GPU.

## Reviewed benchmark contract

One JSON file contains `schema_version: 1`, an `assets` array and a `pools` array. Include **all assets used across training, validation and test**, not only evaluation candidates: leakage checks can inspect only supplied records.

Every asset needs these fields:

| Field | Meaning |
|---|---|
| `id` | Unique garment-observation ID, also used by rankings |
| `research_split` | `train`, `validation` or `test` |
| `product_group` | Reviewed conservative identity group |
| `duplicate_group` | Reviewed duplicate/derived-photo group |
| `image_group` | Original photograph group, shared by all crops of that image |

Groups must be nonempty strings. Use consistent dataset namespaces. A reviewed singleton can have its own group ID; unknown identity must not silently become a singleton. Group assignment requires source review and duplicate inspection; this evaluator does not discover duplicates or prove independence. Importer `product_group_candidate` values are not accepted as reviewed groups automatically.

Each group must belong to just one research split. Shared product, duplicate or original-image groups across splits cause failure, including records outside evaluation pools. Group links are checked separately, so connected chains cannot bridge splits. Freeze groups and splits before training-pair mining.

Each pool contains a `query_id` and `candidates`, a list of objects with `id` and integer `grade` from 0 through 3. Queries and candidates must be in the same validation or test split. A candidate cannot share the query's product, duplicate or original-image group. This enforces the initial cross-product experiment. Reuse of a candidate by multiple queries is permitted and induces statistical dependence.

## Human judgments

Judge the visible denim region in the query against each candidate. Compare observed color/tone, wash/fading strength and placement, and silhouette. Preserve visible lighting. Do not judge preferred brands, personal taste, presumed original fabric color, or photographic background similarity.

| Grade | Joint visible appearance |
|---|---|
| 0 | Clearly dissimilar |
| 1 | Some overlap, but substantial differences |
| 2 | Close overall, with noticeable differences |
| 3 | Very close across the visible comparison facets |

This rubric is a starting protocol to calibrate on pilot examples before freezing the benchmark. Keep facet observations and unobservable/uncertain reasons in the annotation working records. Uncertainty is **not** 0: resolve it or exclude the pair/pool before freezing, identically for every method. No automatic mean of facet scores is assumed. Do not use model rankings to change held-out grades. Independent subset review remains pending.

## Input example (synthetic IDs only)

Save as `benchmark.json`:

```json
{
  "schema_version": 1,
  "assets": [
    {"id": "q", "research_split": "test", "product_group": "p-q", "duplicate_group": "d-q", "image_group": "i-q"},
    {"id": "a", "research_split": "test", "product_group": "p-a", "duplicate_group": "d-a", "image_group": "i-a"},
    {"id": "b", "research_split": "test", "product_group": "p-b", "duplicate_group": "d-b", "image_group": "i-b"}
  ],
  "pools": [{"query_id": "q", "candidates": [{"id": "a", "grade": 3}, {"id": "b", "grade": 1}]}]
}
```

Save each method's ranking as a separate JSON file, for example `b0-rankings.json`:

```json
{"q": ["b", "a"]}
```

Rankings must contain exactly the benchmark's query IDs and, per query, every candidate exactly once in descending method-score order. Top-five-only submissions are rejected. Break score ties deterministically by ascending candidate ID before export. No self matches, duplicate IDs, extra IDs, missing candidates, unjudged grades or duplicate JSON keys are accepted.

```sh
python scripts/evaluate.py --benchmark benchmark.json --rankings b0-rankings.json --output b0-report.json
python scripts/evaluate.py --benchmark benchmark.json --rankings b1-rankings.json --output b1-report.json
```

Keep benchmark bytes identical for B0, B1 and FT, and compare their recorded `benchmark_sha256`. Ranking-file checksums are also recorded. Tune only on validation; report test separately. Output files must not already exist; validation failures do not create reports. Store actual private benchmark files and reports under ignored `data/private/` and `runs/` directories as appropriate, not beside these illustrative snippets.

## Metric and limits

`nDCG@5 = DCG@5 / ideal DCG@5`, gain `2^grade - 1`, discount `log2(rank + 1)` for one-based rank. Ideal order uses **the entire judged candidate pool**, even when a relevant item falls below position five in a submitted ranking. Pools shorter than five use their available candidates; report includes their sizes. Freeze pool-size policy before a real comparison.

All-zero pools have undefined nDCG, recorded as JSON `null` and counted as `zero_positive_queries`. Split-level means exclude them, reporting both scored and total query counts; if none are scoreable the mean is also `null`. Validation and test are never averaged together.

Tests cover hand-computed discounts/gains, perfect and below-cutoff rankings, zero-positive handling, exact pools, uncertain grades, group leakage, and CLI output protection. Synthetic fixtures validate software behavior only. The evaluator does not implement embedding extraction, B1 reranking, group assignment, paired confidence intervals, significance testing or fine-tuning. Future uncertainty analysis must account for shared products/candidates rather than assume every query is independent. Fixed-pool results do not establish full-catalog retrieval performance.
