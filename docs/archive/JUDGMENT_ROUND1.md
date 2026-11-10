# Single-rater calibration — October 26, 2026

The user will judge visible similarity. Codex prepares images, provenance, blind presentation and validation; it does not assign relevance grades. This is a single-rater feasibility study. Agreement with this rater is useful evidence of an operational appearance criterion, but does not establish agreement among typical users. Repeated items measure within-rater consistency, not inter-rater reliability.

## Prepared private packet

- Three Commons wearing-photo crops, 24 previously reviewed GLAMI denim crops.
- Full Cartesian pool: 72 unique query/candidate pairs plus three separated repeat trials, 75 trials total. No model-ranked candidate selection or model scores displayed. Deterministic shuffled candidate order within each query.
- Commons page IDs 509784, 42805504 and 1490243. Sitting, bent legs and partial waist/thigh views deliberately expose visibility limitations; do not infer hidden silhouette. The ambiguous overlapping two-person view was excluded.
- Crop bytes and upstream package checksums retained. Observed lighting retained. Rectangular crops contain some background, shoes or upper clothing; no segmentation or color correction claimed.
- Creator, source and license notices embedded in the private sheet. Commons metadata supplies CC BY licenses; GLAMI publisher card supplies Apache-2.0. Source metadata does not independently establish all depicted-person rights. No raw photos, packet, individual product records or labels committed.
- Product/variant/near-duplicate identity remains unresolved. Research split is null. This packet is **calibration only**, excluded from final held-out claims; do not convert unknown identities into singleton groups to run the strict evaluator.

The original 10 selected reference photos and earlier taste answers are not relevance labels. These three queries are a small purposive pilot, not representative Pinterest inputs.

## Rater task

Open the private `judge.html`, compare only visible color/tone, wash/fading and silhouette, and select 0 (very different), 1 (some overlap), 2 (close), 3 (very close), or U (cannot judge). Judge resemblance rather than preference. Missing visibility can be recorded as an observation reason; use U when it prevents a defensible overall comparison.

Scores are saved in the same browser's local storage, keyed by packet checksum. Export JSON at pauses and completion; browser storage is temporary, not a durable backup. Work on a laptop/desktop for detail inspection. Send the exported JSON back to Codex. The export contains trial IDs/grades/reasons, not photographs. Changing browser/origin does not transfer temporary answers.

## Reproduce / validate

```sh
python scripts/build_judgment_packet.py --queries data/private/judgment_round1/queries.json --gallery data/private/judgment_round1/gallery_assets.json --output data/private/judgment_round1/packet
python scripts/import_judgments.py --packet data/private/judgment_round1/packet/packet.json --ratings path/to/denim-round1-judgments.json --output data/private/judgment_round1/imported.json
```

Output paths must be new to prevent overwrites. Gallery assets were prepared from saved Kaggle crop/metadata outputs in private notebook version 362201537. The 1,338,683-byte gallery package has SHA256 `1a20b9e99a37915986d0daccf653f8afade44c0b47e749eb924d5151d497fc25`. Only this small human-annotation package was transferred locally; bulk images and model weights remain remote.

The importer verifies packet checksum, export identity, unique known trial IDs and integer 0–3/U grades. Partial exports report missing trials. U is never zero. Consistent repeats count once; conflicting repeats require review and are excluded from unique judged pairs until resolved, without averaging. Preserve the raw export as evidence. Import output remains calibration data, not a benchmark.

## Verified now / next

35 local tests pass. Separate synthetic-image UI fixture verified score 0, U with reason, navigation, reload restoration and an actual JSON download with the expected two records. The real sheet loaded both images with zero grades assigned; 390-pixel viewport check found no horizontal body overflow. No real human judgments, agreement estimate, retrieval metric or fine-tuning result exists yet.

After this round, inspect U frequency, repeat conflicts and adequacy of the candidate pool with the user. Freeze the rubric before collecting a larger, independent evaluation set. Review product/duplicate groups and splits before training-pair construction; retain an untouched test set. Compare B0, B1 and the adapted model on the same fully judged held-out pools. A second independent rater on a subset would support a broader human-validity claim; it is not required to begin this explicitly single-rater pilot.

## Received judgments

The actual 75-trial user export was received and validated on October 26, 2026. Packet checksum matched; all known trial IDs appeared once, with no missing trials and no U responses. The earlier two-answer synthetic UI export was distinguished by its packet checksum and was not imported as research judgments. Raw export and validated individual records remain private.

Two of the three repeat pairs received exactly matching grades. One pair received 0 and 1; it remains unresolved and is excluded rather than averaged or selected after seeing model scores. Three repeats are too few to establish stable rater reliability. No extra adjudication is required to inspect the other calibration judgments.

| Usable unique pairs | Grade 0 | Grade 1 | Grade 2 | Grade 3 |
|---|---:|---:|---:|---:|
| Q1: sitting view (23) | 15 | 5 | 2 | 1 |
| Q2: bent legs (24) | 9 | 4 | 6 | 5 |
| Q3: partial waist/thigh (24) | 13 | 5 | 6 | 0 |
| Total (71) | 37 | 14 | 14 | 6 |

The 20 grades at 2 or 3 are observed close matches under the rater's criterion, not an estimate of retrieval success. Candidate presentation was shuffled, not a model result. Zero U responses do not establish full silhouette visibility in the partial queries. Preserve this as a 71-pair calibration collection with one unresolved pair, not a fully judged 72-pair benchmark. Aggregate provenance: [received-judgment report](verification/judgment_round1_received_20261026.json).

Next compute milestone: extract frozen query features remotely, compare B0/B1 rankings descriptively with these labels (explicitly as calibration), then use disagreements to improve the next data/label collection. Q1's incomplete pool must not enter the strict complete-pool evaluator. Final unseen-group metrics and adaptation still require reviewed groups, frozen splits and independent labels; this collection is not silently promoted to test data.

## Remote comparison prepared

`scripts/analyze_calibration.py` revalidates the raw export against its packet, feature crop hashes, 768-D embeddings and pinned frozen-model provenance. It shares grade-independent B0/B1 scoring with the strict baseline CLI; the strict CLI still validates groups, splits and complete labels first. It never creates placeholder identity groups. Missing/U/conflicting labels remain unknown in the top-five display; only fully judged pools receive descriptive calibration nDCG. The w=0.5 control is fixed from the pre-label pilot, not searched using these judgments.

`notebooks/frozen_calibration.ipynb` prepares a remote-only run over the exact 27 reviewed crops. The ignored private `denim-calibration-input.zip` includes crop/source notices, the reviewed extraction manifest, original packet/ratings and the Python source for the run. Three Commons CC BY 2.0/2.5/3.0 crop licenses/attribution and visual geometry were reviewed for this private frozen-feature use; this does not claim independent product identity, general depicted-person rights or publication clearance. Raw inputs and outputs must remain private.

Local preflight verified all 27 crop hashes and required review fields. Notebook cells compile, and all 38 local tests pass, including identical ranks despite changed relevance, withheld metric on incomplete pools, and crop/model provenance rejection. **GPU execution and actual calibration metrics remain pending**: the browser inventory returned no connected browsers during this preparation. A request to reopen the existing Kaggle tab is pending; this is a compute-access block, not a dataset-approval requirement. Prepared artifact hash: [remote preparation report](verification/calibration_prepared_20261026.json).
