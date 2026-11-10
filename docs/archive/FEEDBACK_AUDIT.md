# External-feedback audit — updated October 25, 2026

## October 26 follow-up

- Actual 27-image calibration completed and saved in private version 362288134; comparison/features files verified in its output tree. Q2 B0/B1 nDCG@5: 0.640659/0.639945; Q3: 0.529635/0.446854. Q1 remains incomplete. These are two descriptive, single-rater queries, not generalization evidence.
- The researcher redirected priority to data collection and fine-tuning. First real-label last-block fine-tuning is now complete: 40 steps, training hinge 0.079425 → 0.018524, block checkpoint restoration verified. See TRAINING_PILOT.md. No further standalone starting-model validation is planned.
- Current PROJECT_STATE is a short research status, with internal operation history archived in ignored private storage. DATA_ACCESS no longer reproduces mailbox searches or contact operations. Historical commits still contain old text; no history rewriting was performed. Existing author email/history was not changed without a chosen replacement identity.
- README now declares AI-assisted implementation/screening and human-only relevance judgments. It distinguishes publisher license metadata from image/checkpoint publication clearance. OPEN_SOURCE_REVIEW is now English, consistent with the main research documentation.
- Limitations remain: a clean catalog gallery, only three training queries, incomplete product groups, one rater and a 0/1 disagreement. The current loss uses only clear 2/3-versus-0 relations. Clarifying the boundary and adding mixed-background/query diversity remain necessary for a larger label round; old labels were not changed after seeing scores.
- All 39 local tests pass. Source-data expansion was prepared but not executed before a user-requested pause; more documents/tests are not counted as additional model evidence.

The table below preserves the earlier audit and its then-current test counts.

Review scope: the five criticisms pasted into the project conversation, compared with the current committed scripts, tests, documentation and Git history. One researcher running small fixed-pool experiments is the assumed workload. This is not an independent model-quality evaluation or a whole-repository security audit.

| Feedback | Outcome after this audit | Evidence / remaining work |
|---|---|---|
| No real retrieval result | **Execution partly addressed; quality unresolved** | 24 reviewed real GLAMI crops encoded on T4; exploratory B0/B1 neighbor boards saved. No human-judged baseline metric, fine-tuning or effectiveness claim. See SCREENING_PILOT.md. |
| README too long; first screen unclear | **Addressed in this update** | Concise README with a status table and short run instructions; previous detailed research narrative moved to RESEARCH.md. No fabricated demo image or result is added. |
| DeepFashion2 dependency; no contingency | **Alternative data acquired and screened** | 900 open-license screening images acquired/audited. ABO pilot rejected as unsuitable; 24 GLAMI crops visually reviewed and encoded. Broader crop/product-group review remains. |
| Recovery gaps and one-commit history | **Partly addressed** | New evaluator replaces the missing implementation; Git now has incremental recovery, documentation, evaluation and baseline commits. Original planning documents and legacy UI source remain missing; recovery provenance is retained. |
| Tests cover importer, not evaluation risks | **Addressed for implemented evaluation and audit** | Twelve evaluator tests cover metric/pool/leakage risks. Importer, baseline/crop, acquisition and audit checks bring the local total to 28 passing tests. |

Shared benchmark validation is reused by ranking and evaluation. The CUDA extractor now runs on reviewed real crops; crop/identity/rights flags alone still do not establish review. Paired uncertainty, split assignment and full-catalog evaluation remain unfinished.

The feedback is **not all completed**. Real-data execution is now recorded; the main evidence gap is human-judged, product-disjoint effectiveness and actual fine-tuning. Original lost files remain missing.
