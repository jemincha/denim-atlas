# Real-image screening pilot — October 25, 2026

The acquired 900 files were screening candidates, not 900 denim pants. All 900
passed a fresh SHA-256 check and EXIF-oriented decoding. Decoded RGB pixel hashes
found 900 distinct images; this does **not** rule out near duplicates or shared
products. Every original short side was at least 224 pixels.

## Visual inspection changed the usable-data estimate

Codex inspected all 19 contact sheets (48 images per sheet, final sheet partial).
The ABO 600-image pilot was overwhelmingly denim-print phone cases, with shoes
and one brown-trouser view. No usable denim pants were selected from it. The
original title-only `jeans` screen was too broad. Its acquisition helper now
rejects common phone/case/cover/shoe terms; that change has a regression test but
has **not** been used for a new acquisition. The old outputs remain intact.

GLAMI's 300 images include actual pants, but also cycling shorts, multiple-item
images and uncertain materials. Thumbnail review does not establish that every
remaining item is denim. A purposive pipeline pilot selected these 24 clear,
single-garment front views using the combined manifest's zero-based indices:

```
608 613 615 617 619 628 629 632 633 635 638 640
642 643 644 645 650 651 652 656 658 659 663 666
```

This is an AI visual review, not independent human ground truth or a representative
sample. The selection demonstrates processing; it cannot establish catalog-level
retrieval quality. No personal preference filter was used.

## Processing and artifacts

[`scripts/audit_screening.py`](../scripts/audit_screening.py) validates image paths,
source hashes and decoding, records dimensions/pixel hashes, and generates indexed
contact sheets. It refuses reuse of an existing output directory. The CLI keeps
bulk image work on Kaggle; synthetic tests call its function on tiny local images.

The remote pilot proposes a bounding box from grayscale absolute difference from
white, threshold `>35`, with three pixels of padding. Each of the 24 resulting
crops was then inspected on an enlarged sheet before recording reviewed status.
The crop is saved as RGB PNG without recoloring or white-balance correction.
Residual background and the original 228×298 resolution limit wash detail;
cropping can reduce the short side below the encoder's input size.

Private saved CPU notebook:
[900 Image Audit, version 1](https://www.kaggle.com/code/jemincha/denim-atlas-900-image-audit?scriptVersionId=361851236).
Its 51 saved files include the audit script, 900-row manifest, exact-duplicate
groups, 19 contact sheets, visual-review record, 24 crop PNGs, crop manifest with
hashes/boxes/source references and enlarged crop sheet. The acquisition notebooks
are pinned as version-1 inputs. The first summary-print cell had a missing `json`
import after the audit completed; the next cell imported it and printed the saved
report. This did not require rerunning or overwriting the audit.

The aggregate audit report records zero confirmed items **before** visual review;
the separate visual-review record records the later 24-image pilot. Keep the
two stages distinct. Source images and per-image manifests stay outside Git.

## Evaluation boundary

The existing frozen extractor successfully encoded all 24 reviewed crops on Tesla
T4 into finite 768-dimensional vectors. Model revision and weight checksum match
the earlier smoke check; this run records Python 3.13.15, torch 2.11.0+cu128,
OpenCLIP 3.3.0 and the actual preprocessing. Exact provenance is in
[`verification/real_denim_pilot_20261025.json`](verification/real_denim_pilot_20261025.json).

[Real Denim Feature Pilot, version 1](https://www.kaggle.com/code/jemincha/denim-atlas-real-denim-feature-pilot?scriptVersionId=361864828)
preserves features, scripts, 24-query exploratory rankings and two neighbor boards.
Each query ranks the other 23 images, with self excluded. B0 uses normalized
cosine; B1 uses the documented mean-RGB blend with an illustrative fixed `w=0.5`.
This weight was not optimized or selected for the eventual experiment. All
rankings pass an exact 23-candidate/self-exclusion assertion. Four queries are
shown; all 24 rankings are retained. No placeholder grades were supplied to the
evaluator. On the displayed dark-flare example, adding color changes the top
neighbor from a lighter distressed flare to a darker flare; this is an observation
about these images, not evidence that one method is better overall.

No research splits, verified independent product groups, human appearance grades
or training pairs have been assigned. Original GLAMI `source_split` and its
precomputed similarity fields are not our research split or relevance labels.
No nDCG score or fine-tuning improvement follows from this pilot. Next, review
additional crops and product/variant/near-duplicate links, freeze groups and
splits, then collect human comparisons on fixed pools.
