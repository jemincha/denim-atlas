# Next remote data run

The application is user-reported submitted; access email/password has not been verified. No protected archives have been downloaded. Do not re-submit or email maintainers automatically. Never commit the access password or signed application.

After obtaining access and verifying the intended remote usage scope, download/extract only the needed partition on remote compute. Do not run collection processing or download model weights on the old laptop.

Run the metadata preparation on Kaggle CPU using paths of the actual extracted archive:

```sh
python scripts/prepare_deepfashion2.py --annotations /kaggle/working/DeepFashion2/train/annos --source-split train --output /kaggle/working/deepfashion2_train_screening_v1
```

The path above is an example, not a claimed dataset location. The output directory must not already exist. A `summary.json` with `complete: true` marks a fully validated pass; a partial directory after any failure must not be treated as complete.

Outputs preserve annotation checksums, trousers boxes in original xyxy pixel coordinates, source domain, pair/style IDs and unreviewed denim/rights/group status. No crop is generated until source images and bounds are inspected. No research split or positive/negative relevance label is generated.

Process one original partition at a time. Pair IDs are namespaced by that partition; this does not establish independence across the original train and validation partitions. For the initial study, construct train/validation/test research groups within one acquired original partition after reviewing duplicates and identities. Keep all styles sharing one source pair ID together conservatively. Source identity is not appearance relevance.

Next after import: visually confirm denim, inspect masks/occlusion and crops, verify groups, then freeze a candidate-pool judgment rubric. Existing same-item retrieval labels do not replace cross-product appearance judgments.
