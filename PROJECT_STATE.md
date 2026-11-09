# Denim Atlas — 2026-11-05

Goal: better cross-product denim matching than a specified strong general multimodal
comparator, preserving photographed lighting/wear. Silhouette and surface remain
separate. No taste profiling, original-color restoration or app UI.

## Current handoff

Latest update (2026-11-09): **both retest passes measured; silhouette closure/write-up proposed,not enacted;training paused**.
Both locked passes validated72rows/18comparisons/16source groups,109.31min gap,canonical A/B reversal,protocol/timestamps;immutable private direction_retest_v1.csv,metrics only after full validation,no original-score edits.
C「두 축 모두 비동점이었던 쌍에서의 방향 신뢰성 상한 참고치」:silhouette17/18=94.4%[82.4,100],surface13/14=92.9%[75,100];first/retestU0/18 and0/18 silhouette,4/18 and4/18 surface. C excludes firstU,counts secondU wrong,U/U never match.
DIRECT models(a) first direct choices,shape/surface:FS16/18(88.9%)/9/14(64.3%),CLIP11/18(61.1%)/11/14(78.6%),DINO12/18(66.7%)/9/14(64.3%). Stable subset(b):FS15/17/9/13,CLIP10/17/10/13,DINO11/17/8/13;no score-derived preferences pooled,CI display only.
Fixed decision:silhouette FS88.9%>=C-10pp84.4% -> propose termination/write-up,not automatic closure;surface C92.9% and retestU22.2% pass prespecified measurement thresholds,no「측정 불가 축」classification and no automatic surface learning. Await research-direction approval,no further judging/training/API/GPU/original-size auxiliary now;selected old-dual-nontie known-image evidence,not general ceiling or fresh-product/fine-wash superiority.
18-item plan explicitly approved;pre-start5-line amendment fixed in latest SPRINT_REVIEW. C label is「두 축 모두 비동점이었던 쌍에서의 방향 신뢰성 상한 참고치」;firstU/18 and retestU/18 separately reported,firstU excluded from C/model(a),secondU wrong,U/U notagreement.
Only after BOTH locked passes:compare all3 frozen models with(a)first-direct A/B and(b)stable equal A/B directions,denominators explicit,score-derived results separate. Silhouette decision uses(a)only:FS>=C-10pp -> closure proposal,otherwise silhouette-only group-count learning-curve design proposal(no training).
Surface thresholds accepted unchanged:C<80% OR retestU/18>30% ->「측정 불가 축」for this block/input,exclude from learning design;no post-result adjustment. Between passes no model comparison,C/instability calculation or model-result display;only operational completion/time/storage checks. Wait for both finished passes,no automatic start or answer filling.
Approved R2 block prepared:18 comparisons,4 high-origin/14 low-origin,16 known reference source groups;eligible BOTH old axes numeric/non-tied(5high+25low comparisons),source short side720 cutoff,seeds20261109(selection)/20261110(first order+positions)/20261111(retest order),rule frozen before sampling.
36 screens/72 axis choices,estimated15–21 active minutes plus>=30-minute gap,next day recommended;224white-square images only,separate protocol9d6783767b4a777f11fa37a6388fe105c37285a23419e3980f01613897db03ec. Private ceiling_selection.csv+ceiling224 data and runs/prepare_ceiling_block.py;no new research document/JSON.
Prior visible landing at http://127.0.0.1:8883/judge.html?ceiling=1 was inspected without agent-started judging;researcher has since finished both passes. Isolated tests pass first-pass lock,30-minute gate,shuffled reversed retest,72-row canonical export;no browser human answer synthesized.
C uses matching canonical directions/first-direct A-or-B count;secondU wrong,firstU excluded from C AND all3 model denominators,U/U notagreement;tie notoffered/unresolvable usesU,coverage+both-answered conditional rates separate. Cached FS/CLIP/DINO compare same block first DIRECT choices,never mixed with score-derived preferences;point-estimate R2 unchanged,no training/paid API/original-size auxiliary.
Qwen official conclusion corrected:이 입력 형식에서 순서 불일치 71~78%로 비교 불성립, 범용 모델 대비 우열 미측정. Selected consistent subsets(e.g.14/15) are not superiority evidence;old counts remain diagnostic history only.
Result v2:3 non-evaluation fixtures/6 smoke calls then180 main calls completed,no OOM;parser-only bare-two-line normalization repair,prompt/FP16/224 unchanged;all raw answers revalidated,immutable CSV private.
Qwen3.5-9B fixed-denominator silhouette14/53(26.4%) vsFashionSigLIP37/53(69.8%);surface4/40(10%) vs27/40(67.5%). Answered-only14/15(93.3%) and4/10(40%);matchedFS12/15 and7/10.
Order disagreement:64/90 silhouette,70/90 surface;eligible38/53 and30/40.All finalU are order-inconsistent;invalid-format0/180.Paired onlyQwen/onlyFS3/26 and1/24;consistent subset3/1 and1/4;CIs descriptive only.
R2 selected:global silhouette difference-43.4pp failsR1 althoughconsistent subsetdifference+13.3pp.Propose one12-anchor matched224 A/B/U retest block x2(24screens,48axis choices),active10–15min estimate plus>=30min break;no judging launched,original3/9 gate unchanged,independent C still unmeasured,no training/API/paid/quantized fallback.
2026-11-09: researcher approved revised Qwen comparison;old pending3 rules replaced by R1/R2 in latest review.180 AB/BA main calls after3 non-evaluation synthetic fixture trios x2 smoke calls,unchanged prompt/FP16/224input,OOM stops;no original-resolution auxiliary,no paid/quantized fallback.
Canonical order reconciliation and parser self-checks pass;reuse existing kernel metadata to private jemincha/denim-atlas-qwen35-evaluation-comparator with existing approved private crop dataset,label-free requests embedded in launch code;no new JSON created. Private job actual slug jemincha/denim-atlas-qwen35-evaluation-comparator;v1 loaded FP16 but stopped before main on bare U/U smoke format;parser-only fix verified unchanged promptSHA,v2 COMPLETE.
R1:Qwen silhouette>=FS+10pp with same positive direction on matched order-consistent subset (including U/U as wrong);otherwise R2 minimal ceiling block proposal only,no new judging/training now. CI display only,all claims Qwen3.5-9B-relative;old3/9 gate and human truth unchanged.
New priority per researcher:direction reliability -> one free general-VLM comparator -> approved decision rules before outputs -> error hypotheses;no new human judging/training/paid API/annotator search,nDCG@3 retired from primary decisions(old results retained).
Partial direction proxy:including ties silhouette18/18,surface8/14(4 U excluded);strict at BOTH times13/13 and8/8,conditional on excluding tie transitions,not an identified independent human ceiling. Numeric exact repeats8/9 and3/9 remain unchanged.
Matched model discordances only-first/only-second:FS-CLIP13/9 silhouette,9/5 surface;FS-DINO13/11,10/9;CLIP-DINO9/11,6/9. Model denominators53/40;excluded-pool comparisons3/18 andhuman ties34/32 sum to90 derived comparisons/axis.
Comparator prepared,NOT run:Qwen/Qwen3.5-9B@c202236235762e1c871ad0ccb60c8ee5ba337b9a,free private Kaggle2xT4 FP16,no API/CPU/offload/quantized fallback;same68 crops/224white squares,90 derived reference/A/B comparisons,seed1108;requests.csv checksum8059492dc74242aabf30a6c9e960d9a2036308e82f72e46c83f45fc193a41ca8,pinned prompt/parser in runs/general_comparator_20261108/run.py;runtime fit/quota/compatibility untested.
Gate waiting:show protocol/prompt and approve3 review rules before execution;actual full direction ceiling C remains unidentified,so ceiling-dependent decisions2/3 cannot trigger from conditional100% proxies. Model outputs are comparator predictions only,never truth/training labels;no error-analysis detour or goal narrowing now.
Latest Downloads denim-direct-preference-v1.csv validated18/18 rows across9 anchors:
protocol/packet/rater/axis/query/A-B positions match;immutable source archived privately
as data/private/frozen_human_20261105/direct_preference_v1.csv. Private analysis script
runs/analyze_direct_supplement.py validates completeness and transition self-checks.
Silhouette:7 strict choices+2 ties;FashionSigLIP5/7,CLIP2/7,DINOv22/7 strict agreement.
Surface:5 strict+3 ties+1 unknown;FashionSigLIP1/5,CLIP4/5,DINOv23/5.
Versus original first-session pair relations:silhouette8 same+1 tie->strict;
surface6 same+2 strict->tie+1 unknown;no strict reversal among observed relations.
Versus partial repeated-score relations:silhouette8 same+1 tie->strict;
surface6 same+1 strict->tie+2 unknown. Only one candidate was originally repeated.
Source notes flag reference-photo detail/color readability in2 cases;do not infer
new hard labels from notes. Model ties receive0.5,human tie/unknown excluded from
strict concordance denominators. Counts are post-hoc diagnostics,not new endpoints.
Original pool eligibility differs:8/9 supplement anchors eligible for silhouette,
only3/9 for surface;6 surface anchors were excluded in main analysis. Thus new
surface model ordering is not evidence of regression or a protocol-driven gain.
No combined/revised original scores,metrics or approved3/9 surface reliability gate;
no repeat direct-choice test or independent new-product/general-VLM superiority.
Next analyze existing common model disagreements and crop/readability limits;
no immediate further human task,training,teacher-label promotion,API or GPU run.
Connection recovery:3 task-owned servers shared8883;verified their command lines,
stopped only those processes,and launched runs/serve_supplement.py as one hidden
loopback server with exclusive Windows port binding. Host HTTP200 verified.
The generated page repeated embedded image data across3 modes(67,171,044 bytes),
exceeding browser transport framing;replaced UI-only data URIs with68 verified local
crop paths,reducing HTML to161,070 bytes;generator preserves this fix on rebuild.
Actual visible IAB tab6 shows9 cases,0/18 choices and CSV control;27 judgment photos
loaded successfully(the28th image is unused zoom placeholder). Tab marked deliverable.
No human answers,packet bytes,original scores,protocol or frozen metrics changed.
Researcher approved direct A/B/tie/unknown supplementary evaluation. Private
runs/prepare_supplement.py adds ?supplement=1 to existing judge.html, preserving
original/explanation modes and all frozen data.9 original repeat anchors x2 axes;
each pair uses the repeated candidate and lowest-gallery-index other pool candidate,
without scores/models/labels for selection,then order/A-B randomized(seed1108).
Protocol hash677344ff3eee8b5fdc0db722baee737095065192184d8a5a9cdf7908a3e67317;
separate browser storage and CSV export denim-direct-preference-v1.csv,optional notes,
tie/unknown distinction,zoom and storage-failure lock. Synthetic nine-case,selection,
autosave/reload,CSV and failure-lock checks pass;no real answers filled or collected.
New workspace local endpoint http://127.0.0.1:8883/judge.html?supplement=1;
initial browser opening failed;subsequent exclusive-server/payload recovery above
verified actual right-side visibility and photo loading. Ready for human judging.
This9-pair familiar-image pilot cannot establish full-pool/retest reliability or
replace original3/9 failure gate;no training/API/GPU,goal change or new research JSON.
Existing9-repeat post-hoc analysis (runs/analyze_repeat_diagnostics.py) validates
99-trial provenance and classifier self-checks; no source grades/metrics edited.
Silhouette:8 identical numeric repeats,1 one-point change;18 partial candidate
relations unchanged. Surface:3 identical numeric repeats,4 one-point changes,
1 U->U,1 numeric->U;no2/3-point changes. U reasons cite color/detail uncertainty.
Holding the two un-repeated candidates at first-session grades, surface18 partial
relations comprise8 unchanged,3 tie->strict,3 strict->tie,4 unknown;0 strict reversals.
Only one candidate per query was repeated, so this is a partial sensitivity check,
not independently repeated full-pool ordering or proof of stable preference.
The approved3/9 surface exact-nonunknown gate still fails. Narratives plus this
diagnosis suggest grade-boundary/observability sensitivity, not proven causal weights
or demonstrated encoder improvement. Direct A/B/tie/U supplement is now approved
as above,not replacement of frozen gates/grades;teacher labels,training/API/GPU
and goal changes remain outside the authorized follow-up.
Qualitative response received for all4 displayed diagnostic cases;8 axis-specific
narratives are private data in data/private/frozen_human_20261105/explanations.csv.
All4 selection-axis preferences preserve original ordering after clarification.
The previously unassigned surface narrative is now confirmed; private source data
records shared wash patterns with a closer photographed blue tone as the deciding cue.
Descriptions identify continuous leg-width profile, spatial whisker/thigh sanding,
damage/texture absence and flat-vs-worn photo uncertainty. These are observed human
criteria, not proven encoder failure mechanisms. One weak new surface preference
was previously an equal-grade pair; preserve this distinction, never revise scores.
The4 selected examples are not the9 repeat tests and cannot explain or overturn
the3/9 surface reliability result. Next map human criteria to existing examples;
no regrading/training/new metrics or goal change.
Latest qualitative follow-up: researcher volunteered natural-language explanations
for model-human agreement/disagreement examples. Four distinct-anchor cases were
selected from valid complete pools:2 axes x(all3 models agree/all3 reverse), with
human candidate grade gaps2–3. Order/A-B randomized with seed61106; model identities,
scores, agreement category and prior human grades hidden during initial explanation.
Private preparation code: runs/prepare_explanation_cases.py; existing judge.html
has an explanation-only mode at ?explain=1&case=1, leaving packet/rating storage intact.
Selection assertions and combined JS syntax pass; automatic visibility check failed,
but researcher subsequently inspected all4 cases and supplied narratives in chat;
explanations are diagnostic only, no score revision or training.
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
