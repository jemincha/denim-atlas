# Open-source reuse review

Reviewed October 26, 2026 using official repositories, model cards and documentation. OpenCLIP/Marqo are already used in the remote pilot. The other candidates have not been installed or benchmarked for Denim Atlas. Adoption decisions below are engineering judgments for a small single-rater study on Kaggle, not measured improvements.

## Decision

Retain OpenCLIP 3.3.0 and the pinned Marqo-FashionSigLIP checkpoint. First compare the same crops, pools and judgments under B0/B1. Consider SAM 2 only if inspection supports background/garment isolation as a failure source. Learn query-conditioned appearance ordering rather than product identity. Do not train and evaluate on the same three calibration queries.

| Project / primary source | Capability and license | Proposed use | Decision |
|---|---|---|---|
| [OpenCLIP](https://github.com/mlfoundations/open_clip), [license](https://github.com/mlfoundations/open_clip/blob/main/LICENSE) | CLIP/SigLIP loading, preprocessing and training; MIT | Frozen extraction now; limited image-encoder adaptation later | Retain verified 3.3.0. Do not assume current main features exist in this version or upgrade during a comparison. |
| [Marqo-FashionCLIP](https://github.com/marqo-ai/marqo-FashionCLIP), [FashionSigLIP card](https://huggingface.co/Marqo/marqo-fashionSigLIP) | Fashion embeddings and public benchmark evaluation; repository/model card Apache-2.0 | Existing 768-D starting checkpoint; reference evaluation practices | Retain model. Published seven-dataset results do not establish denim appearance retrieval quality. |
| [PyTorch Metric Learning](https://github.com/KevinMusgrave/pytorch-metric-learning), [explicit triplets](https://kevinmusgrave.github.io/pytorch-metric-learning/losses/) | Losses, miners, distances and reducers; MIT | Explicit query/closer/less-similar triplets from ordinal human judgments | Conditional. Use existing PyTorch for a simple loss if sufficient; add library when mining complexity justifies it. |
| [SAM 2](https://github.com/facebookresearch/sam2) | Promptable image/video segmentation; core code/checkpoints Apache-2.0, third-party components separately noted | Box/point mask proposals, reviewed before a background-isolation ablation | Candidate, not adopted. Official requirements include Python >=3.10 and torch >=2.5.1; verify a separate remote environment. |
| [FiftyOne](https://github.com/voxel51/fiftyone), [similarity docs](https://docs.voxel51.com/user_guide/similarity.html) | Visual dataset curation, embedding search and duplicate review; OSS Apache-2.0 | Inspect crops, provenance, groups, relevance and failures at scale | Defer. Static sheets/JSON suffice for 27 images; similarity is not proof of shared product identity. |
| [FAISS](https://github.com/facebookresearch/faiss) | CPU/GPU dense-vector search and clustering; MIT | Accelerate normalized embedding search when catalog scale becomes a bottleneck | Defer. Unnecessary for 24 candidates; indexing does not train a better representation. |

## Adaptation hazards

The [metric-learning example](https://github.com/KevinMusgrave/pytorch-metric-learning#using-losses-and-miners-in-your-training-loop) forms positives from shared class labels. Our pairwise similarity is not a transitive class: different products may look alike, and one product can look different under wear or lighting. Neither product ID nor grades 0–3 should be passed as global class labels. Construct explicit within-query relations inside the training split; the [indices_tuple API](https://kevinmusgrave.github.io/pytorch-metric-learning/losses/) supports these without class labels.

OpenCLIP's image-text losses/CLI do not automatically solve image-image ordinal ranking. Reuse loading/preprocessing and adapt the supervision. The [3.3.0 loss source](https://github.com/mlfoundations/open_clip/blob/v3.3.0/src/open_clip/loss.py) was inspected; no new training loss has been run.

SAM 2 requires prompts and mask review, not automatic semantic truth. A mask may cut out fading or include another garment. Preserve the rectangular-crop baseline and measure masking as a separate ablation. Existing B1 uses all crop pixels; garment-only RGB is a different control and must retain its own preprocessing/hash provenance.

Near-duplicate search complements exact hashes but cannot distinguish shared products, derived photos and visually similar independent products without review. Embedding proximity proposes candidates; it must not automatically merge identity groups.

## Sequence and acceptance criteria

1. Execute the fixed 27-crop calibration comparison. Q1 is incomplete and receives no metric; Q2/Q3 numbers remain descriptive, not held-out claims. Preserve actual outputs before calling the run complete.
2. Inspect failures. If garment/background separation appears material, propose a small reviewed SAM 2 ablation and compare mask quality and ranks before scaling.
3. Expand diverse queries and mixed-background/hard candidates. Review product/duplicate groups, freeze splits, and collect another human-label round. Keep a final test set untouched.
4. Start with the minimum ranking objective. Introduce metric-learning miners only if needed; pin versions, check gradients/restart behavior and select settings on validation only.
5. Add FAISS/FiftyOne only when search speed, memory or review workload becomes an observed bottleneck. No extra vector service or app UI is needed now.

Software/model licenses do not grant image collection or publication rights. Candidate inspection is not installation, successful integration or evidence of improved accuracy. Publication of raw images or derived weights requires separate source/artifact review.
