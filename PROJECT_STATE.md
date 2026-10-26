# Denim Atlas — status, 2026-10-27

Small study of visible denim similarity across products: color/tone, wash/fading and silhouette. No personal-taste objective, original-color reconstruction or app UI.

## Evidence

- GLAMI: 1,200 verified images, including the earlier 300; 12,434,870 image bytes. Official full-archive MD5 verified. Codex inspected 512 name-filtered images and whitelisted 347; blue/gray studio imagery is overrepresented.
- Expanded weak image/text adaptation completed on Kaggle T4, private job `denim-atlas-glami-text-fine-tuning` version 3: 347 images, 2 epochs, 44 steps, last vision block (7,087,872 parameters). Fixed-batch training loss 0.865115 → 0.823334; 85,070,133-byte checkpoint and block restoration verified. No human similarity-quality score.
- Earlier human-label pilot: 75 trials / 71 usable pairs, 27 images, 40 steps; training hinge 0.079425 → 0.018524. Its three queries are training data for that earlier experiment.
- All three existing query cases had identical ranked top-5 before/after adaptation in the same 347-image gallery; no demonstrated retrieval improvement.
- Official Kaggle CLI 2.2.5 authentication and remote CPU/GPU execution verified. Browser automation is no longer required. 43 local tests pass.

## Limits and next gate

Raw data/ratings/weights remain private. Publisher metadata is not independent clearance for seller images or checkpoint publication. Product groups, near duplicates and independent splits are unresolved; fine wash detail is limited by low-resolution images. Source descriptions are weak supervision, not human relevance labels.

Paused at the researcher's explicit sprint-stop request. All submitted remote jobs finished; the localhost annotation server was stopped. Files and browser-local draft state are retained. Do not resume experiments until requested.

Resume at `data/private/judgment_round2/packet/judge.html`: 3 queries × 17 candidates + 3 repeats = 54 trials. No grades were assigned by Codex and no new human export has been received. Restart its localhost server if needed; import the researcher's JSON through the existing provenance-checking importer, then construct training pairs. This is additional calibration/training, not independent held-out evaluation. Existing starting-model validation is finished; access-request status needs separate verification.

See [expansion/protocol](docs/GLAMI_EXPANSION.md), [training evidence](docs/verification/glami_text_finetune_20261027.json), [evaluation](docs/EVALUATION.md) and [feedback audit](docs/FEEDBACK_AUDIT.md).
