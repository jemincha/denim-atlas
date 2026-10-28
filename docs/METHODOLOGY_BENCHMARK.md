# Methodology benchmark and sprint reset — 2026-10-29

Research review, not a new training result. Primary papers, author repositories and engineering guides were inspected. Recommendations below are our proposed adaptations; their effectiveness on Denim Atlas is untested.

## Assessment

The task is fine-grained, cross-product visual similarity with a consumer-photo domain gap. A pretrained encoder, embedding/ranking objective and human relevance evidence fit this task. The project has completed execution/debugging pilots; it has not established effective transferable denim adaptation. The important gap is varied, task-aligned supervision and representative evaluation, not another pretrained-model selection exercise.

Observed evidence: 347 screened weak-text training images; the later relevance continuation used only three queries, 17 candidates and 51 unique judged pairs. Its 71 constructed triplets are combinations of those judgments, not 71 independent observations. Training-pool nDCG@5 increased 0.4493 → 0.8526, but three different query images yielded 0.3841 → 0.3513. This supports reporting unsuccessful transfer in this small pilot; it does not identify a general statistical effect or prove its cause. [Recorded results](verification/new_query_round3_results_20261029.json).

## What to benchmark

| Source | Method actually described | Adaptation to this project | Boundary |
|---|---|---|---|
| [PyTorch transfer-learning tutorial](https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html) | Pretrained networks used as frozen feature extractors or fine-tuning initializations | Retain the existing FashionSigLIP backbone; compare a small trainable component with the current last-block approach only after supervision is usable | The tutorial is classification, not evidence that either option improves denim retrieval |
| [Full Stack Deep Learning: debugging](https://fall2019.fullstackdeeplearning.com/course-content/training-and-debugging/debug) | Execute the model, fit a tiny batch, then compare with known implementations or simple controls | Treat completed tiny-data fitting as a finished debugging gate; move to broader data and a controlled experiment | Repeating tiny-set fitting is not new generalization evidence |
| [ASEN, AAAI 2020](https://arxiv.org/abs/2002.02814), [author loader](https://github.com/Maryeon/asen/blob/master/image_loader.py) | Attribute-conditioned embeddings; existing attribute values determine triplets; separate training/validation/test material | Use color/tone, visible wash and silhouette as distinct supervision axes; construct relationships from actual attribute annotations | A shared color label is not a positive overall-appearance label. The paper's fashion attributes do not establish denim-wash coverage |
| [Conditional Similarity Networks, CVPR 2017](https://openaccess.thecvf.com/content_cvpr_2017/papers/Veit_Conditional_Similarity_Networks_CVPR_2017_paper.pdf) | Different similarity notions use different embedding subspaces | Make conflicts between surface appearance and shape inspectable, initially with simple facet-specific signals | Full reproduction or an elaborate multi-branch architecture is not required for the next pilot |
| [BAPPS/LPIPS author protocol](https://github.com/richzhang/PerceptualSimilarity#c-about-the-dataset) | A reference and two alternatives support relative perceptual judgments; repeated human observations are recorded | Trial an A/B closeness question for ambiguous training comparisons, with both-unsuitable and uncertain responses | It studies distorted patches, not cross-product fashion. Do not claim its model or measured timing transfers to our task; relative preference is not absolute relevance |
| [Batch Active Learning at Scale, NeurIPS 2021](https://research.google/pubs/batch-active-learning-at-scale/) | Batch selection combines uncertainty and diversity to reduce redundancy | Compare a small diverse/uncertain selection against a random audit under the same human budget | Current cosine scores are not calibrated confidence; merely showing top-k is not a demonstrated active-learning method |
| [A Metric Learning Reality Check, ECCV 2020](https://www.ecva.net/papers/eccv_2020/papers_ECCV/papers/123700681.pdf) | Comparable training conditions, validation-separated tuning, disjoint groups and multiple runs | Keep groups together before pair mining; choose settings on validation; compare identical pools; repeat promising runs with several seeds | Our relevance grades do not equal identity classes. Retain nDCG@5 and positive precision rather than copying identity metrics indiscriminately |
| [DeepFashion2 official task](https://github.com/switchablenorms/DeepFashion2#consumer-to-shop-clothes-retrieval) | Consumer-to-shop retrieval uses corresponding clothing identities/styles | Borrow crop, occlusion and cross-domain evaluation ideas | Identifying the same product is a different target from matching visibly similar different products; its labels and published scores are not our ground truth |

ASEN is the closest methodological reference among the reviewed work. Its author implementation was inspected: it selects a specific attribute and samples images with matching/different values for the triplet. This shows a route to generating training relationships from reusable annotations rather than individually grading every image pair. Repository environment requirements are old (Python 3.6 / PyTorch 1.1); no code was installed or copied, and license/modern-runtime compatibility was not established. Borrow the supervision structure before considering implementation reuse.

## Changes justified now

1. **Audit supervision before collecting another large archive.** For already acquired images, inventory source resolution, views, capture/product groups and actual usable annotations. Build a per-facet table of known/unknown labels and provenance. Check whether proposed datasets contain the needed annotations; broad fashion categories alone are insufficient. [Fashionpedia](https://arxiv.org/abs/2004.12276) illustrates localized attribute annotation, not guaranteed coverage of our wash definitions.
2. **Define one learnable first hypothesis.** Example: reliable observable tone and broad silhouette supervision improves these facets on new capture groups. Keep fine wash/fading unknown where labels or resolution cannot support them. This narrows an experiment without changing the overall matching goal. Product descriptions can describe intrinsic color rather than photographed color; treat mismatches as weak/unknown, preserve observed lighting and avoid whitening/color-jitter that erases the target.
3. **Separate reusable weak supervision from human reference labels.** Attribute positives constrain only the corresponding facet. Do not call every different product a negative or every same product a positive. Machine-generated attributes need confidence/provenance and a small human audit. A smaller head is a candidate lower-capacity control, not yet a selected replacement; identify labels first. Report head-only adaptation honestly if used.
4. **Use people for selected information.** Codex handles acquisition, cropping, deduplication, candidate mining and presentation. The researcher checks ambiguous distinctions and sampled label quality. Use query-specific pools; start with a 5–10-question workload cap per request. Include random/coverage checks because our narrow model-selected pools missed two positive pairs. That cap is an operating choice, not a literature sample-size rule or proof of annotation efficiency.
5. **Keep evaluation protected.** Training-label selection can prioritize useful cases; evaluation must retain bad returned candidates and complete pool judgments. The existing new-query round is now development evidence. Do not repeatedly optimize against it and later describe it as a fresh test. Build genuinely new capture/product-group material for a final claim; capture separation alone is not proven product separation.
6. **Run small, interpretable experiments.** Reuse the frozen reference and the proven remote pipeline. Fix data/preprocessing/pools, change one training signal or capacity choice, log validation behavior, and only repeat promising settings across seeds. More margin/learning-rate sweeps on the existing three training queries do not repair missing supervision.

## Direction and pace

[Google's ML engineering guidance](https://developers.google.com/machine-learning/guides/rules-of-ml) emphasizes usable measurement, a simple initial pipeline and testing infrastructure separately from learning. That supports the setup already completed; it does not make commit count, documentation volume or tests a measure of research progress.

Our completed work is a useful debugging foundation. The sequence then spent too much effort on small human rating grids while task-aligned data and independent groups remained unresolved. Learning from 51 judged pairs with three anchor queries while updating roughly 7.1 million parameters is an unusually narrow pilot, not a sufficient basis for a training recipe. A fitted training score alone did not justify continuing the same loop.

The last continuation's measured training/report segment was 7.39 seconds and the earlier weak-text training loop 14.53 seconds on T4. These exclude setup/download and cover different work; they are not end-to-end throughput benchmarks. We have no reliable human-hours ledger or matched-project timing dataset. No claim about an average number of development days is supported by this review. Available records point to data/supervision, annotation design and orchestration as current constraints, rather than measured GPU training throughput.

Track the following per sprint:

| Progress measure | Report explicitly |
|---|---|
| Usable data | Unique reviewed images and product/capture groups, not ZIP size or derived pair count |
| Learning signal | Known labels per facet, distinct anchors and supported positive examples; weak versus human labels |
| Human cost | Actual questions and elapsed labeling time; useful constraints and coverage per budget |
| Experiment throughput | Complete controlled train → validation cycles, including setup/failures and compute cost |
| Quality | Same-pool metrics, per-query failures, independent groups and uncertainty; failed results count as findings |

## Proposed next sprint, in order

| Work block | Concrete deliverable | Stop/go decision |
|---|---|---|
| 1. Data/supervision audit | Existing inventory plus a small source sample; known/unknown counts for the three facets and source groups | If no usable attribute signal exists, resolve source/label acquisition before writing a new training architecture |
| 2. Reusable training set | A versioned grouped manifest and facet labels with provenance; splits fixed before pair generation | Confirm each trained facet has varied anchors and genuine positive/negative supervision; report gaps |
| 3. Minimal adaptation experiment | Existing encoder, one explicit hypothesis, one trainable configuration and a frozen reference; cached features where compatible | Run real training and validation; make one change at a time |
| 4. Controlled relevance check | Frozen ranks on different capture/product material, small useful human audit, complete judged evaluation pools | Report quality and workload even when results are worse; do not hide false positives |
| 5. Decide the next iteration | Keep, revise data/supervision, or stop the hypothesis based on evidence | Expand only the component supported by results |

Working targets for a later pilot may be 1,000–3,000 usable images and 20–30 diverse query groups, but these are planning ranges, not minimum scientific requirements, promises of data availability, or a reason to request a large manual grid. First establish label feasibility on existing data. A good next sprint produces a broader supervised dataset and one interpretable validation result; a single negative result is more useful than another tiny training-loss improvement.

The proposal does not restart standalone pretrained-model verification, require a mobile UI, or authorize new dataset agreements. No new data transfer, package installation, architecture migration or training job was performed for this review.
