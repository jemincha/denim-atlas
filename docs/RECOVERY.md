# Partial recovery — 2026-10-23

The local workspace was observed empty. A read-only unsandboxed check also found no README or scripts. The cause is unknown. No deletion, reset or cleanup was performed by this recovery.

Recovered code comes from the visible `pre` elements of the rendered saved notebooks, read through the authenticated browser. This preserves displayed code text; it is not an original notebook-file download. JSON was parsed from the visible execution output before the `Report:` / `Output:` suffix, without inventing measurements.

| Source | Recovered artifacts |
|---|---|
| https://www.kaggle.com/code/jemincha/denim-atlas-gpu-readiness?scriptVersionId=361374829 | check_remote_gpu.py, check_remote_model.py, check_remote_backward.py, recovered_gpu_checks.ipynb, gpu/model/backward check JSON |
| https://www.kaggle.com/code/jemincha/denim-atlas-data-audit?scriptVersionId=361384852 | inspect_fashionpedia.py, recovered_data_audit.ipynb, fashionpedia_audit JSON |

The saved model source resolves the original short revision `c56244c` to a full SHA before downloading. That original code is retained as recovered. Exact resolved SHA and weight checksum are in the recorded model report. Pin the full SHA in the eventual training recipe.

No GPU work was rerun and no model/checkpoint weights or image collections were downloaded locally during recovery. Restored Python syntax and JSON were checked. Recovered notebooks have empty execution counts/outputs to avoid implying local execution.

README and PROJECT_STATE are newly reconstructed status documents based on this conversation and saved results, not recovered original files. Previous evaluator, tests, planning documents, source handoff and legacy UI are still missing. Prior historical test claims are not rerun results for this partial tree.
