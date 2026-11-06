# Denim Atlas — 2026-11-05

Goal: better cross-product denim matching than a specified strong general multimodal
comparator, preserving photographed lighting/wear. Silhouette and surface remain
separate. No taste profiling, original-color restoration or app UI.

## Current handoff

Latest update (2026-11-06): **measured; research gate waiting, adaptation paused**.
User fixed the three decision rules before output interpretation. Frozen Kaggle v2
completed;68 features/model at768/512/384 dimensions pass model/crop/input-manifest
provenance and preprocessing checks. V1 recorded the last crop hash as weight hash;
fixed variable collision and reran identical models/data; v1 is excluded from analysis.
Human preference concordance (95% anchor-bootstrap CI): FashionSigLIP silhouette
69.8%[57.7,82.0],surface67.5%[53.7,81.5]; CLIP62.3%[47.2,76.4],57.5%[40.0,73.2];
DINOv2 66.0%[51.8,80.0],65.0%[46.2,81.8]. Random concordance50%.
Exact nonunknown repeats: silhouette8/9,surface3/9; reference only, not a hard ceiling.
Silhouette29 complete pools/28 nonzero pools/53 strict preferences; surface24/21/40.
Unknown/conflicting-repeat pools excluded by axis; zero-gain pools have no nDCG.
FashionSigLIP nDCG@3 .944[.908,.975]/.899[.830,.958]; CLIP .901[.854,.943]/
.853[.771,.927]; DINOv2 .908[.857,.953]/.857[.778,.932]. Random .873/.829.
All paired between-model nDCG difference95%CIs include zero. Approved rule3 applies
because surface repeats3/9<7/9: descriptive claims only, no adaptation or goal reduction.
High/low source-resolution slices are confounded with natural/catalog wearing:
silhouette6/23 complete anchors (5/23 nonzero), surface4/20 (4/17 nonzero).
Pure catalog query anchors0; every gallery image is catalog228x298, so independent
wearing/catalog effects, detailed-wash quality and strong-general-VLM superiority
remain unmeasured. Existing repeat disagreements are the next diagnostic evidence;
no additional human labeling/training/model search is authorized by this result.
89 Python tests and synthetic browser JS checks pass (tests use workspace temp dir).
User explicitly approved private crop/manifest transfer. Private Kaggle dataset
jemincha/denim-atlas-frozen-human-inputs was created; frozen-human-comparison
kernel version1 was pushed with NvidiaTeslaT4 and3600-second limit; corrected v2 is COMPLETE.
Only frozen feature extraction; no labels, adaptation or paid API. Decision rules
are approved in the latest review. Privacy inspection passed for15 selected text files: no raw photos/ratings/features, JSON, runs/auth scripts, binary files or secret-pattern findings.
Researcher completed delayed repeats. Latest Downloads export
`denim-frozen-human-20261105-v1-judgments (1).json` passes packet provenance validation:
90 primary pairs and9 repeats complete on both axes,198 decisions,0 missing.
Existing authenticated Kaggle read succeeds. Archive CRC/69 allowed entries and
embedded source compilation pass. Initial automatic upload rejection was resolved
by explicit user approval; only inputs.zip (68 crops and manifest) was uploaded,
with no labels/secrets. CLI Windows upload path error resolved by running in dataset folder.
Feature extraction was not started during judging; this timing deviation is recorded.
Frozen model scores and repeat agreement were evaluated only after rule approval;
these are single-rater fixed-pool development measurements, not final quality proof.
Evaluation sheet now renders10 pairs per page with autosave, zoom, storage-failure
lock and delayed9 repeats only after90 complete pairs,30 minutes and a new tab session.
Synthetic JS behavior checks and15 related Python tests passed; browser visual QA pending.
Prior automated visibility check failed; researcher has since used/saved the sheet.
Existing private judge.html was rebuilt,
preserving frozen packet bytes and pools (30 preselected anchors x3 candidates;
randomized presentation only, no documented random/hard strata).
Do not launch GPU until the judging sheet is ready and visibly available; then follow
the user's fixed order, with approved decision rules before any result interpretation.
No rankings inspected, new compute/training/authentication, commit or push on restart.

Current restart point: Kaggle OAuth is restored and a real API read succeeded as
`jemincha`. Do not repeat login or annotator/API-credit exploration. Resume the
prepared frozen comparison below; its GPU run and human judgments are still pending.
Local HEAD is `e1e4811`; the comparison code/state changes are uncommitted and must
be preserved. No new research report/verification JSON; use the existing review.

Sprint1/2 technical execution is recorded; **research gate pending**. The frozen
FashionSigLIP/two-head run is a pipeline check; 3 machine-judged anchors cannot
resolve the quality hypothesis. The recorded preference-agreement count is unchanged.
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

B/quality superiority and detailed washing remain the goal. The researcher approved
about30–40 minutes (estimate) for independent human evaluation only; training labels
remain delegated. Latest approved order: existing Qwen/human error decomposition,
frozen embedding comparison, human judgments, then the current visual assistant's
agreement-gated supervision and group-count learning curves. No annotator search.
Human-only evaluation truth and pre-fixed stop criteria are required before comparison.
No paid general-model budget has been approved.
Error review is complete: on the matched8 photos,2B family7/8/lightness5/8;
4B family5/8/lightness6/8. Fifteen historical attribute/run errors comprise2 observed
anchor-sensitive cases and13 unresolved causes; localization/incapacity is not proven.
The private frozen-only bundle has30 wearing queries,38 candidates,90 pairs plus9
delayed repeats,198 axis decisions,5 per batch. Six queries are high-resolution;
24 queries and all gallery images remain228x298. Fine-wash evidence remains limited.
Local86 tests pass; GPU execution is untested. On2026-11-05 official SDK loopback
OAuth completed; `runs/kaggle-login/status.txt` is `api_verified` and a separate
`kaggle kernels list --mine` succeeded. There is no remaining authentication gate.
No new teacher labels, training or paid API calls.

## Immediate continuation (same project checkout)

1. Inspect `runs/frozen_human_20261105/`: private dataset input archive and metadata,
   `run.py`, and `kernel-metadata.json`. These are prepared, not uploaded/executed.
   The archive's68 crop hashes and ZIP CRC were verified; the embedded runner was
   syntax-checked. It runs the three pinned encoders sequentially, no adaptation.
2. Upload the input dataset privately as `jemincha/denim-atlas-frozen-human-inputs`
   (check existence first; do not overwrite an unrelated artifact), then push the
   private kernel `jemincha/denim-atlas-frozen-human-comparison` on free Kaggle T4.
   Use current CLI help, keep sources private, and do not use any paid API/cloud.
3. Download only small feature outputs, verify input/model provenance and dimensions.
   Human evaluation packet is `data/private/frozen_human_20261105/packet.json`,
   hash83d382802878564e44f088f86c4a142effd13abe166e45f5a227ebf56025501a.
   `source_crops.csv`, `protected_groups.csv`, `fixed_methods.csv` preserve inputs.
   The UI is `judge.html` in that directory; localhost8882 was HTTP200 verified.
   If needed restart Python http.server bound127.0.0.1 with this exact directory.
4. Open http://127.0.0.1:8882/judge.html in the RIGHT Codex tab and verify it is
   actually visible before requesting the first5 judgments. A queued open is not
   visible. Do not use open_in_codex terminal session IDs to attach exec PTYs: it
   previously opened an unrelated PowerShell, causing a mistaken credential paste.
5. Total99 screens/198 independent-axis grades (90 pairs+9 delayed repeats), estimated
   25–41min, unmeasured. Record actual first-batch time; never fill human scores.
   Protocol/stop rules are frozen in the packet and latest review. No new machine
   supervision or adaptation before the human evaluation gate. Teacher checks later
   use the current visual assistant, not a newly searched model; report its unexposed
   checkpoint and limit any coarse calibration pass to the attributes actually tested.

The30 anchors are wearing photos but only6 are high-resolution natural scenes;
24 anchors and all38 gallery images are228x298. This is a diagnostic development
comparison, not a final detailed-wash or strong-general-VLM superiority benchmark.
The original quality-first goal remains; public embedding comparisons do not prove
superiority over a strong general multimodal model. All evaluation groups are
excluded from future training; learning-curve size means garment/capture groups.

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
