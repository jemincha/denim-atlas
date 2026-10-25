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
