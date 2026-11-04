# Denim Atlas — 2026-11-05

Goal: better cross-product denim matching than a specified strong general multimodal
comparator, preserving photographed lighting/wear. Silhouette and surface remain
separate. No taste profiling, original-color restoration or app UI.

## Current handoff

Sprint2 completed: frozen FashionSigLIP regional features and two separately trained
projection heads. **No development preference-agreement gain.**
[Experiment](docs/REGIONAL_AXIS_PILOT.md) · [Review003](docs/SPRINT_REVIEW.md) ·
[Plan](docs/DEVELOPMENT_PLAN.md).

- 27 observations /54 views, train18/development9 protected folds;13 train constraints,
  6 development constraints. Labels are the conversational visual assistant's weak
  judgments, not human truth; exact teacher checkpoint/repeat accuracy unavailable.
- E0 garment/E1 regional/E2 trained: development silhouette2/3 and surface2/3 for
  all three. E2 fixes1/regresses1 silhouette preference; surface winners unchanged.
  Training reaches7/7 silhouette,5/5 surface plus1 tie; loss0.066095->0.00006586.
- 200 fixed AdamW steps, seed37,64-D heads,147,456 parameters; encoder remains frozen.
  Dev-gradient exclusion and exact saved-head prediction restoration passed.
  84 local tests passed; CPU-recomputed E0/E1 outcomes match GPU output.
- Private TeslaT4 kernel `jemincha/denim-atlas-regional-axis-pilot`,version2,complete.
  Encoder loading/features44.70s; encoding/training/save46.71s excludes setup/queue.
  Weights remain remote/private; no pending compute job, paid API or new human labels.
- Small private results/cache: `data/private/regional_heads_20261105/`.
  Original packet/teacher: `data/private/regional_sprint1_20261105/`.
  [Public result/hash record](docs/verification/sprint2_results_20261105.json).

## Next execution — revised plan after Sprint 2

Review snapshot: S2-2026-11-05. The [revised plan](docs/DEVELOPMENT_PLAN.md) replaces
older forward-work instructions; historical experiments/results stay unchanged.
Sprint 3 now closes evaluation coverage and exact strong-comparator access/version
before further adaptation. Include axis-conflicting/wearing cases, protected groups,
readable detail and judgments frozen before system rankings. Distinguish machine
teacher reproduction from independent human-quality evidence.
Sprint 4 tests one controlled improvement; Sprint 5 freezes and evaluates the final
recipe. No automatic backbone expansion, manual training grid, paid API use or
color-only replacement goal. [Sprint 2 implementation/result commit](https://github.com/jemincha/denim-atlas/commit/1bcc00b).

## Carry-forward limits

No independent human matching-quality gain or strong-general-model superiority.
Historical human-continuation nDCG declined0.3841->0.3513; source-fit proxy gains
remain distinct. All96 rejected Qwen attribute drafts stay outside training.
All1,200 cached sources, including562 screened images, are228x298; supplied metadata
has no original URL fields. Fine weave/detail and wearing-domain quality remain
unmeasured. Known groups do not certify distinct products. Strong-comparator exact
version/access and independent evaluation truth remain later gates. Source-image
and checkpoint release rights are not cleared; raw material stays private.

At each sprint boundary update this state and `docs/SPRINT_REVIEW.md`, compare actual
work with the approved flow and brief limits/next investigation in Korean. Continue
authorized work to a genuine human/access gate. Any later human comparison images
must be visibly opened in a right-side Codex tab; queued is not visible.
