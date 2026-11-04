# Denim Atlas — 2026-11-05

Goal: better cross-product denim matching than a specified strong general multimodal
comparator, preserving photographed lighting/wear. Silhouette and surface remain
separate. No taste profiling, original-color restoration or app UI.

## Current handoff

Sprint1 is complete for a **machine-supervised regional pilot**. The researcher
explicitly delegated training judgments to the visual assistant; no manual training
annotation gate remains. [Input contract](docs/SPRINT1_INPUT_CONTRACT.md) ·
[Alignment review002](docs/SPRINT_REVIEW.md) · [Plan](docs/DEVELOPMENT_PLAN.md).

- Private cached-source audit:1,200/1,200 image hashes and562/562 reviewed hashes
  verified; every audited source is228x298. Supplied metadata has no original URL
  fields. Enlarging images does not recover weave or tiny wash details.
- Frozen packet:27 known source groups,54 source-derived regions,10 anchor cases;
  train18/development9 protected against known-group/file/decoded-pixel leakage.
- 20 machine decisions:18 strict preferences,1 distance tie,1 neither.19 usable
  constraints; strict training anchors silhouette7/surface5, development3 each.
  Neither/U never become zero grades; no absolute relevance grades inferred.
- Teacher: this Codex conversation's multimodal visual assistant. Exact checkpoint
  unavailable; no separate ChatGPT API call or paid API use. Labels are weak,
  outputs frozen; repeat consistency and accuracy are unestablished.
- Raw packet/ratings/training inputs: `data/private/regional_sprint1_20261105/`.
  Source audit: `data/private/source_audit_20261105/`. Public aggregate/hashes:
  [readiness](docs/verification/sprint1_machine_readiness_20261105.json).

## Next execution

Start Sprint2 with the pinned FashionSigLIP encoder: cache garment and hip/thigh
features, compare E0/E1 and two small axis projections E2 on the frozen packet.
Use train only for fitting. Development preference agreement measures teacher
reproduction; it is not independent human acceptance or superiority to GPT.
Do not expand last-block training before diagnosing the head experiment.

## Carry-forward limits

No regional-head training or independent quality improvement yet. Historical
human-continuation new-query nDCG declined0.3841->0.3513; source-fit proxy gains are
not appearance quality. See [fit](docs/FIT_PROXY_EXPERIMENT.md) and
[human continuation](docs/HUMAN_ROUND2.md). All96 rejected Qwen attribute drafts
remain outside training. Current folds are development material, mostly catalog
views; known groups do not certify distinct products. Strong-comparator exact
version/access and independent evaluation truth remain later experiment gates.
Source-image/checkpoint release rights are not cleared; raw material stays private.

At every sprint boundary update this state and `docs/SPRINT_REVIEW.md`, compare
actual work with the approved flow, brief remaining evidence gaps in Korean,
and continue authorized work until a genuine human/access gate. Human comparison
artifacts, if needed later, must be visibly opened in a right-side Codex tab.
