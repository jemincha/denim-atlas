# Wearing-photo supply pilot — October 26, 2026

## Commons: actually acquired small screening previews

The official Commons API returned two bounded category pages: Men wearing jeans
and Women wearing jeans, at most 50 files each. There were 99 distinct file pages
(one overlaps categories). An explicit canonical license-URL screen retained 43
CC0/CC BY candidates. The first 24 by page ID were downloaded as small previews,
image-verified and hashed: **1,769,414 bytes**, no failures. No high-resolution
originals or model weights were downloaded locally.

The local private directory `data/private/commons_wearing_20261026/` contains raw
API snapshots, original/preview URLs, creator/credit/license metadata, hashes,
24 previews, a contact sheet and `review.html` with source and attribution links.
The HTML escapes source metadata. Generated data stay out of Git; the aggregate
report is [verification/commons_wearing_20261026.json](verification/commons_wearing_20261026.json).

Codex inspected all previews. Four image views (indices 00, 08, 09, 20) are worth
further garment crop/mask review: crossed seated legs, two skateboarding poses,
and two seated subjects in one frame. These give five garment targets, not five
independent products. 08/09 appear to share one capture session; keep them
together conservatively. The two targets in 20 overlap, so a rectangle can mix
garments. Other previews include tiny, cut-off, occluded, monochrome and group
scenes. They were not silently assigned negative relevance or non-denim labels.

This is a supply/visual-triage pilot. Canonical license metadata is not independent
verification of authorship or all personality/privacy rights. Source review,
target crops/masks, product groups and human relevance judgments remain pending.
No images have been marked training-ready or fed to an encoder.

Sources: [Commons reuse guidance](https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia),
[men category](https://commons.wikimedia.org/wiki/Category:Men_wearing_jeans),
[women category](https://commons.wikimedia.org/wiki/Category:Women_wearing_jeans).
This first-page, first-ID sample is not representative of the full repository.

## Unsplash Lite: user-authorized remote metadata audit

The user explicitly accepted the official Dataset Terms on October 26 and
authorized remote Kaggle metadata screening. This does not authorize public
redistribution of source images or metadata, or establish permission to publish
weights/example photos. [Official dataset](https://github.com/unsplash/datasets)
and [terms](https://github.com/unsplash/datasets/blob/master/TERMS.md).

The official Lite endpoint returned a ZIP of **320,024,071 bytes**, downloaded
only on Kaggle CPU. SHA-256:
`aa0fcb859040ed64e93817d1d878d0c6f861763283261ba1a6aa5d8d4af6aec6`.
Actual filenames are `photos.tsv000` and `keywords.tsv000`; the audit handles
numbered TSV parts. Archive contents include metadata, not original photos.

The audit streamed **25,000 photo rows and 909,055 keyword rows**. A whole-word,
case-insensitive `jeans|denim` screen selected **293 unique photo records**:
260 keyword matches and 60 human/AI-description matches (these overlap).
These are textual candidates, not confirmed pants or wearing photos. Denim
jackets, ambiguous scenes and AI keyword errors can be included. No personal
preference filter or assumed positive/negative pairs were used.

Packaged terms were preserved and their normalized text matched the current
official `TERMS.md`. The audit saves candidate IDs/URLs/descriptions/creator
usernames privately, excluding unnecessary precise location fields. Aggregate
checksums/counts may be recorded; raw licensed records stay private.

`scripts/audit_unsplash.py` processes an already-downloaded licensed ZIP, performs
no image requests and refuses bulk laptop execution. Fixture tests cover numbered
TSVs, deduplicated keyword joins, candidate-only status and output protection.
Any later preview inspection is a separate stage, not part of the metadata
audit's `images_downloaded: 0` record.

That preview stage also completed on Kaggle: **24 resized images, 2,163,607 bytes**,
chosen deterministically by sorting SHA-256(photo_id) among the 293 candidates.
Codex visually triaged all 24. Six views (08, 12, 14, 15, 16, 20) warrant further
crop/mask review; other views include uncertain material, tiny/occluded pants,
denim jackets, scenery and objects. This does not establish six independent
products or six training-ready observations. Preserve partial views as an input
condition; do not invent missing wash detail or label ambiguity as zero relevance.

The private [Kaggle metadata audit, version 1](https://www.kaggle.com/code/jemincha/denim-atlas-unsplash-lite-metadata-audit?scriptVersionId=362186247)
stores the source archive, matching terms, audit code, 293-row candidate manifest,
24 previews, contact sheet and stage reports. Aggregate evidence:
[metadata](verification/unsplash_lite_metadata_20261026.json) and
[previews](verification/unsplash_lite_previews_20261026.json).
Source records and pictures are not committed or reproduced in this document.

Local validation: 32 tests pass, including the new Commons URL/license screen
and Unsplash TSV join checks. No model inference or fine-tuning was performed
on either new wearing-photo pilot.

## Plan A preparation

[PINTEREST_ACCESS_BRIEF.md](PINTEREST_ACCESS_BRIEF.md) records the exact permission
questions and official routing channel. It is an unsent technical brief. No
Pinterest platform permission or creator license has been obtained.
