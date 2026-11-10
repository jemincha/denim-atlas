# Frozen B0/B1 runbook

Updated October 25, 2026. Local synthetic tests exercise scoring, color statistics and the ranking-to-evaluation CLI. The extractor has now run on remote T4 CUDA for 24 reviewed GLAMI crops; see [SCREENING_PILOT.md](SCREENING_PILOT.md). Exploratory neighbor boards have no human relevance labels or research-quality score.

## Order and current stopping point

1. Obtain images with permission for the intended remote processing.
2. Confirm denim, create and visually review garment crops, resolve product/duplicate/original-image groups and freeze research splits.
3. Freeze candidate pools and collect human relevance judgments using [EVALUATION.md](EVALUATION.md).
4. Export a reviewed crop manifest; extract frozen features on Kaggle GPU.
5. Run B0/B1 on validation; choose and record the B1 weight there (or predeclare it).
6. Run the unchanged recipe on test once. Inspect failures before selecting a fine-tuning recipe.

Open-license images and a 24-crop processing pilot are available. Product/duplicate review, frozen research splits and human judgments remain unfinished; the exploratory pilot does not satisfy steps 2–3 for a scored benchmark.

## Crop input

The extractor accepts already reviewed, opaque RGB garment crops, not whole outfit photos or raw dataset annotations. Keep file paths relative to a private image root. It validates paths, review status and SHA-256 before requesting the model. Status flags record an actual review; setting them does not itself establish permission.

Example manifest structure (replace placeholders with reviewed records):

```json
{
  "schema_version": 1,
  "assets": [{
    "id": "same-ID-as-benchmark",
    "crop_file": "crops/example.jpg",
    "crop_sha256": "REPLACE_WITH_ACTUAL_FILE_SHA256",
    "usage_status": "approved",
    "denim_status": "confirmed",
    "crop_status": "reviewed"
  }]
}
```

Keep rights/provenance and crop-review evidence separately with the private data records. Include all query/candidate IDs for the selected benchmark. Hash crop bytes after review. Use these exact crops for every method. Verify that IDs and crop hashes match the frozen benchmark's crop records; the evaluator validates supplied identities/groups, not their real-world correctness.

## Remote feature extraction

Use a Kaggle CUDA runtime and the repository checkout. The installation below follows the previously verified OpenCLIP release; the full remote dependency environment must still be checked and saved for this run.

```sh
python -m pip install open_clip_torch==3.3.0
python scripts/extract_features.py --manifest /kaggle/working/private/crops.json --image-root /kaggle/working/private --output /kaggle/working/features.json
```

Paths are examples. This CLI refuses laptop execution and CPU fallback. It freezes all model parameters, uses batch one and FP16 CUDA autocast, downloads only the OpenCLIP config/weights at revision `c56244cc94f92419e8369fa71efdaf403b124ce8`, and checks the weight SHA-256 against the earlier verified file. It does not modify the older smoke-check scripts or train a model.

The artifact records each crop hash, normalized image embedding and mean RGB, plus model revision/checksum, manifest checksum, preprocessing representation, relevant package versions, Python/CUDA/device and batch size. Output must be new. Failures before writing do not produce a feature file; interrupted writes may leave a partial JSON that must be discarded. Save remote outputs privately before stopping the session.

Color is the full reviewed crop's arithmetic mean RGB after EXIF orientation, scaled to `[0,1]`, with no white balancing or de-fading. The encoder uses its published preprocessing on the same oriented crop. Their spatial reductions differ: a single color mean loses wash placement and detail. Any residual background influences this control; inconsistent crops can confound the experiment. No segmentation or background-color invention is performed. Test this deliberately simple control before considering a more complex color descriptor.

## Scoring and evaluation

The feature JSON contract is `schema_version: 1`, optional `provenance`, and `assets` keyed by observation ID. Each asset has a finite nonzero `embedding` vector and three `mean_rgb` values in `[0,1]`. The runner renormalizes embeddings; all used vectors need identical dimensions. Unused feature records are ignored. Keep feature extraction and benchmark construction independent of the relevance grades.

- B0 score: `(cosine(query, candidate) + 1) / 2`.
- Color score: `1 - Euclidean(mean_RGB_query, mean_RGB_candidate) / sqrt(3)`.
- B1 score: `(1 - w) * B0 + w * color`, with `w` in `[0,1]`.
- Ties: ascending candidate ID. Both methods rank every candidate in the same fixed pool.

The affine mapping of cosine does not change B0 order; it gives both B1 components the same nominal range. This is a control, not a claim of perceptual color distance or an optimized model. Grades are used only to validate/score the finished order, not to generate rankings. The weight has no default: record a predeclared value or a validation-only choice. The tool does not enforce that historical choice; never search weights on test.

```sh
python scripts/run_baselines.py --benchmark data/private/validation.json --features runs/features.json --color-weight 0.5 --output runs/baselines-validation-w05
```

`0.5` is an example, not a selected research parameter. This lightweight scoring CLI can run locally on feature vectors; image/model processing stays remote. Each new output directory contains B0/B1 full rankings, evaluator reports and a `summary.json` with `complete: true`, feature/benchmark checksums, feature provenance and scoring recipe. If any output step fails, a partial directory is incomplete unless the completion summary exists. Existing directories are never reused. Both reports must share the same benchmark checksum. Embeddings and paths/provenance can still be sensitive: keep actual artifacts private under ignored data/run directories.

No real baseline quality, paired uncertainty, training objective, fine-tuned model or full-catalog performance has been established. These choices require real baseline failures and reviewed data; they are the next research work, not guessed in advance.
