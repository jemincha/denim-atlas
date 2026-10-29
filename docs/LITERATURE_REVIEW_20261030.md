# Denim Atlas: literature review and next experiment — 2026-10-30

Research review requested after the attribute-teacher audit. This report preserves the goal of **better matching quality than a strong general multimodal model on a defined denim task**. Lower cost alone is not the primary success condition. Literature results below were read from primary papers; none were reproduced here. Proposed adaptations are hypotheses, not implemented capabilities.

**Finding**

The closest methodological direction is attribute-conditioned, global-plus-local similarity learning. Our current infrastructure can support it, but our completed fit-only and coarse-tagging experiments have not yet tested it. A precise cross-product denim benchmark and reliable, region-specific training relationships are still missing. No reviewed paper establishes that our available data or training recipe can beat the current ChatGPT model on denim.

The earlier [methodology review](METHODOLOGY_BENCHMARK.md) already cited ASEN and Conditional Similarity Networks. The failure was not simply a lack of references: their attribute-conditioned supervision did not reach an implemented appearance objective. This review extends that reading to the global/local journal model and recent MLLM retrieval comparisons, and makes the experimental decisions explicit.

**1. ASEN: the closest architectural reference**

[Fine-Grained Fashion Similarity Prediction by Attribute-Specific Embedding Learning](https://arxiv.org/pdf/2104.02429), IEEE TIP, accepted 2021; extension of AAAI 2020 ASEN. Read introduction, method, experimental setup and Tables I–V. [Author repository](https://github.com/Maryeon/asenpp).

The model learns attribute-conditioned representations and combines a whole-image branch with an enlarged region selected using attribute attention. FashionAI attribute-retrieval mAP is 60.60 for the global branch and 64.31 for the combined model (Table I). This supports testing complementary local evidence, not replacing all global information with a crop. Supervision uses matching/different attribute values; it is not label-free. Its attributes and relevance definition do not establish denim wash fidelity or GPT superiority. Borrow the architecture principle on our current pretrained encoder; do not port the old training stack wholesale. A shared broad attribute remains only an axis-specific constraint, not proof of overall similarity.

**2. Localized Triplet Loss: the closest supervision reference**

[Localized Triplet Loss for Fine-Grained Fashion Image Retrieval](https://cdn.amazon.science/50/d7/72cd224546dcbb40e50e5b44003f/localized-triplet-loss-for-fine-grained-fashion-image-retrieval.pdf), CVPR Fashion/Art/Design Workshop 2021. Read Sections 3–5 and Tables 1–3. [Author publication page](https://www.amazon.science/publications/localized-triplet-loss-for-fine-grained-fashion-image-retrieval).

Fashion specialists supplied interest points and 10,805 relative comparisons over 4,302 dress photos. Test triplet accuracy was 69.90% with global triplet learning versus 73.72% with localized triplet learning, averaged over three runs. This is narrow, expert-supervised evidence, not modern GPT comparison. Our adaptation should ask which candidate better matches the hip-to-thigh wash region while excluding silhouette from that question, and separately compare silhouette. Avoid random easy negatives and do not require manual tagging of every possible garment property. The paper's local translation regularization is relevant; its color jitter is not automatically appropriate when photographed tone is the target.

**3. LookBench / GR-Lite: a recent fashion retrieval reference, with important limits**

[LookBench: A Live and Holistic Open Benchmark for Fashion Image Retrieval](https://arxiv.org/html/2601.14706v1), January 2026 preprint. Read Sections 3–4, Tables 2–3 and Appendix C. [Released model card](https://huggingface.co/srpone/gr-lite).

Table 3 reports real street-look fine-Recall@1 of 55.15 for FashionSigLIP and 60.14 for GR-Lite. This supports a newer comparator, not an immediate backbone replacement. There is no GPT retrieval row. Training uses product-identity ArcFace supervision and large corpora; GR-Lite includes private training images. Its reported 93% attribute correctness is an LLM-judge estimate, not human agreement. The paper describes a 512-D projection while the released card/Table 3 expose 1024-D embeddings; inspect actual checkpoint behavior before reuse. The card's Apache label does not resolve upstream DINOv3 conditions. Our different-product, observed-appearance positives must not be replaced by identity labels.

**4. Training-free MLLM reranking: the necessary strong comparison**

[Indexing Multimodal Language Models for Large-scale Image Retrieval](https://arxiv.org/html/2604.13268v1), April 2026 preprint. Read Sections 3–4 and Appendix A/Table A. [Author implementation](https://github.com/gkordo/mllm-ilr).

The method compares query/candidate images directly and uses answer-token probabilities for reranking. On ILIAS at 560px, Table A reports mAP@1k of 33.4 without reranking, 24.3 with Qwen-3B, 53.2 with 7B and 51.3 with 32B. Small-model failure does not discredit strong MLLMs, and scaling is not monotonic. These are Qwen2.5-family, same-object retrieval results, not our Qwen3 tagging experiment or cross-product denim scores. Borrow direct image-pair comparison and a strong reference. Do not copy the question “same object?”; our prompt must explicitly permit different products and preserve photographed color/wear. Token probabilities are ranking signals, not calibrated correctness.

**5. LamRA: learning from difficult retrieved candidates**

[LamRA: Large Multimodal Model as Your Advanced Retrieval Assistant](https://arxiv.org/pdf/2412.01720), CVPR 2025; linked preprint submitted December 2024. Read Sections 3.4–4.1. [Project page](https://code-kunkun.github.io/LamRA/).

LamRA separates retrieval and reranking, adapts a multimodal model with LoRA, and mines difficult training candidates from its retriever's top 100. Pointwise and listwise objectives teach relevance rather than generic description writing. Its full training uses multiple A100s, so “LoRA” does not make the published recipe a free-T4 workload. Borrow bounded candidate mining and task-specific ranking supervision, not its training scale. In our task a different product in the top ranks may still be a real positive: verify the relevant axis instead of labeling every unpaired result negative. Copying a teacher alone cannot establish superiority over that teacher.

**6. A Metric Learning Reality Check: experimental discipline**

[A Metric Learning Reality Check](https://www.ecva.net/papers/eccv_2020/papers_ECCV/papers/123700681.pdf), ECCV 2020. Read Sections 2–4 and conclusion.

The study shows how backbone, augmentation, tuning and test-feedback differences distort claimed metric-learning progress. Its class-disjoint protocol does not directly define our graded cross-product relevance. Borrow matched inputs, validation-only selection, repeated promising runs and honest uncertainty. Keep existing nDCG@5 and axis-specific relevance; do not change losses or metrics merely because a paper reports a higher number. Our already-inspected query rounds are development data, not a fresh final test.

**Additional recent work, with lower direct transfer**

[MCMR: Beyond Global Similarity](https://arxiv.org/html/2603.01082v1), March 2026 preprint: read dataset construction, reranking Table 4 and human-study appendix. It tests multiple image/text constraints and reranks a fixed first-stage top-50 pool. Borrow explicit constraint checks and separate candidate availability from ordering. Its natural-language queries, metadata-only conditions and generated evaluation material differ from image-only observed denim matching. Do not import hidden material, price or manufacturing labels into our task, or treat its reranking scores as end-to-end denim performance.

[Exploring Multi-Modal Large Language Models and Two-Stage Fine-Tuning for Fashion Image Retrieval](https://arxiv.org/html/2606.19684v1), June 2026 preprint (author comment: SOICT 2025): read method and Table 1. It combines generated captions with staged training and negatives, but its reported FashionIQ average R@10/50 (55.32/75.67) trails the listed MAPNet result (55.70/76.20). Caption generation is a candidate aid, not a demonstrated universal solution. FashionIQ's modification-text task is different from ours; this is not the principal blueprint.

**What has slowed this project**

These are conclusions from our records, rather than claims made by the papers:

| Current practice/evidence | Implication | Change |
|---|---|---|
| Fit-name supervision improved its source-cut proxy but not convincingly human appearance matching | We optimized a partial proxy | Train on the specific visual relationship to be retrieved |
| Three-query human continuation fitted training judgments but declined on the next small query set | Transfer is unproven; an overfitting explanation is plausible, not established | More distinct anchor groups and a protected evaluation; stop reusing tiny training grids as progress |
| Only 17 human attribute observations; most labels are broad color/brightness | This does not supervise local wash geometry | Use a small number of local, explicitly scoped comparisons; retain unknowns |
| Many GLAMI files are small previews; 228x298 examples have been inspected | Enlarging them cannot restore missing weave or wash detail | Establish visible detail per image; retain source resolution and reject unsupported texture claims |
| Initial pools contained few or no convincing alternatives for some queries | Ranking cannot create a match absent from the gallery | Separate gallery coverage failures, shortlist misses and ordering errors |
| Whole appearance was initially collapsed into one score | One axis can mask another; old labels cannot be decomposed | Preserve independent silhouette/surface labels and diagnostics |
| Repeated weak-teacher prompting | Produces annotation evidence, not retrieval improvement | End this loop; any later teacher labels must pass an axis-specific audit |

There is no matched human-hours/compute ledger to support an “average number of days” comparison. The measured constraints are task-aligned evidence, image coverage and orchestration, not demonstrated saturation of GPU training throughput. Future progress should be counted in completed controlled train/validation cycles and useful cross-product constraints, not commits, documentation or raw pair combinations.

**The testable research claim**

Proposed: *Can garment- and region-aware, axis-conditioned adaptation improve human-judged cross-product denim matching over both frozen FashionSigLIP and a specified strong general multimodal comparator, especially on cases with similar base color but different wash placement or similar silhouette but different surface appearance?*

This is narrower than claiming a universally better fashion model. Report overall representative quality and the predefined difficult slices; do not claim a general win from a selected failure montage. The model is allowed to build on general pretrained vision. The contribution is learning the missing denim relationships, not recreating broad visual knowledge.

**Minimal model and supervision proposal**

Reuse FashionSigLIP, remote execution, grouping, importer and evaluator. Start with two trainable projection heads on cached, frozen features. One receives garment-wide evidence for silhouette; the other receives garment-wide plus reviewed hip/thigh regional evidence for surface. Preserve regional position; arbitrary patch matching can match knee fading to thigh fading. An enlarged rectangular crop is not a segmentation mask, a pose-aligned region or recovered high-resolution detail. Manual development regions can test the hypothesis before building automatic localization.

Train an axis only from observed relationships for that axis; missing/ambiguous labels contribute no loss. Broad color/cut agreement is insufficient to create an overall positive. Mine visually plausible alternatives, retain true positives, and sample both close confounders and diverse examples. A later comparison may unfreeze the last vision block if the head-only model is limited; change this separately. This is an adaptation of literature principles, not a reproduction of ASEN or a claim that frozen features retain all needed detail.

Do not normalize away the target: keep observed lighting, yellow cast, fading contrast and wear. Test global/garment/region differences without adding color jitter or white-balance restoration. Simple continuous color measurements can be a control or supporting feature, but are not a substitute for wash structure or silhouette learning. Generation/upscaling must not fabricate evaluation details.

**Next sprint, ordered by decisions rather than infrastructure**

| Step | Concrete output | Decision before proceeding |
|---|---|---|
| 1. Evidence-ready development set | Reuse reviewed images; record source resolution, target garment, view/occlusion and visible hip/thigh/hem regions. Build candidate groups containing plausible alternatives, with AI suggestions explicitly unverified | If useful detail or alternatives are missing, improve that image supply; do not train from invented positives |
| 2. Small targeted human gate | Show at most 5-10 scoped decisions per interaction, preferably close candidates; compare silhouette and surface separately. Confirm plausible positives rather than another mostly-obvious-negative grid | Confirm that the question is answerable and yields real training constraints; no large manual tagging round by default |
| 3. Matched comparator snapshot | Freeze candidate pools, source groups, pixels, prompts/model IDs and the general-model ranking before training. Use existing judgments only on the axis originally judged | If no strong-model access exists, prepare executable inputs and identify that missing comparison; never substitute 2B/4B tagging as the GPT reference |
| 4. One controlled adaptation cycle | Frozen garment-wide reference, garment+region control, then two-head axis-specific adaptation with the same inputs. Record complete training/validation outputs | Attribute any gain to the changed component; repeat promising settings across seeds before broader claims |
| 5. Fresh quality check | New product/capture groups, blind human relevance, identical pools for all methods; report nDCG@5, top-5 relevance and axis errors | Report gains, losses, coverage and uncertainty. Do not select checkpoints or prompts from this test |

Five to ten queries can debug feasibility, but cannot establish GPT superiority. A later 20-30-query evaluation is an initial planning target, not a statistical sample-size rule; estimate uncertainty at the query/group level, since pair/triplet combinations are correlated. If population-level claims are intended, add independent raters and document disagreement rather than relabeling the author's judgments as universal ground truth.

**Fair comparison against a general multimodal model**

Use two distinct comparisons. First, compare ordering on an identical manageable candidate pool, allowing both systems the same original/garment/region views. Then evaluate the complete search pipeline, including whether it retrieved plausible alternatives at all. A reranker cannot rescue an item outside its shortlist. Partial pool judgments support only pool-conditional relevance/coverage, not full-gallery recall.

Freeze a strong comparator's exact available model/version, prompt, image detail, decoding and date. ChatGPT's self-reported model name alone is insufficient provenance; record UI/API evidence and unavailable controls. Give the comparator an explicit cross-product, observed-appearance instruction, allow uncertainty, and check sensitivity to candidate order on development examples. Do not handicap it with poorer crops, fewer visible details, an identity-matching prompt or an artificially tiny context. Report compute/time separately; the user's primary target is better matching, not a speed-only win.

A strong model may propose training comparisons, but its outputs remain weak labels. Human checks must include agreements, disagreements and random coverage. Do not use the same model's judgments as the only test truth when claiming to beat it, and do not treat a listwise choice or verbal confidence as calibrated similarity. Human-corrected errors and local evidence could permit a student to improve on a teacher; copying it provides no such guarantee.

**Reuse and execution boundaries**

- ASEN/ASEN++: borrow the method; author code link verified in the paper, current repository fetch unsuccessful. No implementation or license compatibility claimed.
- Localized Triplet: primary PDF accessible through Amazon Science; no current dataset-download availability established. Borrow the local-label protocol, not unreviewed dress data.
- GR-Lite: public checkpoint card found, not downloaded or executed. Resolve source/code/license and paper-card output differences before any adoption; keep FashionSigLIP for the first controlled experiment.
- LamRA and MLLM-indexing: author project/code links identified; no dependencies installed, code audit, memory fit or reproduction performed. A full LamRA reproduction is outside the first T4 pilot.
- No new dataset agreement, image transfer, weights, API spending, training job or benchmark score was created by this review. Previously rejected automatic annotations remain quarantined.

**Decision**

Retain the quality-first denim specialization goal. Stop coarse-teacher prompt iteration as the main work stream. The next proposed experiment is **axis-specific global-plus-region matching with reliable cross-product supervision**, measured against a strong general multimodal ranking under matched inputs. Cropping is one controlled component of that experiment, not the research goal. The exact experiment remains a proposal until the researcher confirms the direction and the evidence-ready set exists.
