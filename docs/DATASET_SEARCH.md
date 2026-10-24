# Alternative dataset search — October 25, 2026

## Decisions and execution evidence

| Dataset | Fit for denim appearance research | Access / action |
|---|---|---|
| Amazon Berkeley Objects (ABO) | Original catalog photos, multilingual titles, source listing IDs and multiple views. Useful for a small cross-product pilot; exact ASINs still need variant/duplicate review. | Official CC BY 4.0 image/metadata distribution. Acquired and verified 600 original images remotely on Kaggle CPU from 589 title-screened listings / 875 connected image IDs. No request required. |
| GLAMI-1M | Product/image IDs and fashion categories; lower-resolution default images and multiple languages. Denim needs text/visual screening inside pants categories. | Official publisher's Hugging Face dataset card says Apache-2.0. Acquired and image-verified 300 screening images remotely using range reads of the official ZIP. |
| DeepFashion In-shop | Garment identities, boxes, multiple poses; good complement to catalog-only data. Source identity is not appearance relevance. | Signed agreement and institutional-email request required. User approved the agreement/signature and sending; request sent from the institutional account. Official-page CC address bounced; a copy was sent to the same person's current HKU address. Approval/password and remote-use scope remain pending. |
| DeepFashion Category/Attribute | Clothing types, attributes, boxes. Less direct identity information than In-shop. | Official page says no unzip password needed for this subset. Noncommercial research and distribution restrictions still apply. Did not download the full large collection while the related release request and remote-use clarification are pending. |
| Fashion200K | Cropped fashion products and descriptions; pants available. | Original author's repository supplies a public Drive download and Apache-2.0 repository license, but image-specific grant was not independently established in this check. Lower priority than explicitly licensed ABO/GLAMI. No images acquired. |
| Fashionpedia | Existing 109 source jeans labels in the validation audit are candidates only. | Image terms vary by source; not an automatically cleared replacement. Existing metadata audit retained; no new image acquisition in this search. |

Fashion-MNIST is excluded: 28×28 grayscale cannot support the color/wash detail target. Unofficial mirrors of protected datasets are not used as access substitutes. Data collection is bounded to relevant screening subsets, not every fashion archive.

## ABO acquired subset

Source: [ABO official page](https://amazon-berkeley-objects.s3.amazonaws.com/index.html), [official license](https://amazon-berkeley-objects.s3.amazonaws.com/LICENSE-CC-BY-4.0.txt).

Credit for images/data: Amazon.com. Credit for dataset construction: the ABO creators named in the official README and source page. Cite Collins et al., *ABO: Dataset and Benchmarks for Real-World 3D Object Understanding*, CVPR 2022. Preserve these notices alongside any shared subset and indicate later crops/changes. Acquired originals are unchanged; the manifest is a derived screening index.

The remote run read 147,702 listings, selected 589 English-title jeans/denim-trousers candidates, mapped 875 unique source image IDs and fetched the first 600 sorted IDs. This cap is an acquisition pilot, not representative sampling. All 600 downloads passed image-file verification; failures: 0; image bytes: 133,060,612. Source archive/metadata/license hashes and aggregate evidence are in [the recorded report](verification/abo_acquisition_20261024.json).

Preserved privately on Kaggle in [ABO acquisition output, version 361825214](https://www.kaggle.com/code/jemincha/denim-atlas-abo-jeans-acquisition/output?scriptVersionId=361825214). The saved output tree was checked for the image folder, candidate listings, screening manifest, license and summary. The notebook is private. Large archives and images were not downloaded to the laptop or committed to Git.

`scripts/acquire_abo.py` records source listing relationships, image hashes, image sizes/modes, license/attribution and unreviewed state. Listing IDs do not establish independent products: sizes/colors/markets and reused images need conservative grouping. Titles are screening hints, not visual denim confirmation. Confirmed denim, reviewed crops, relevance labels and research splits remain zero/unassigned in this acquisition report.

## GLAMI acquisition procedure

Sources: [publisher repository](https://github.com/glami/glami-1m), [official dataset card](https://huggingface.co/datasets/glami/glami-1m), [publisher loader](https://github.com/glami/glami-1m/blob/main/load_dataset.py).

`scripts/acquire_glami.py` pins the resolved dataset revision and reads the official ZIP using the remote runtime's installed fsspec. It saves source CSV metadata, source record subsets, image hashes and the source card. It does not extract arbitrary archive paths. Only decimal image IDs are written to the new image directory. No automatic code or model download is part of this script.

The first metadata pass found no category literally containing jeans. An actual taxonomy inspection showed mens/womens/boys/girls pants categories. The corrected screen requires one of those categories plus the English word jeans or denim in name/description. Other-language terms can be missed and descriptions can be false positives: all records stay unreviewed. The corrected source screen found 7,276 rows; the attempted acquisition cap is 300 unique images. Original train/test tags are preserved as source metadata, not trusted as product-disjoint research splits.

The corrected run completed: 300 image files verified, 2,494,479 image bytes, source revision `befda45d8d4e8b8082bb8a1912d1f9eb9483991c`. Aggregate evidence is in [the GLAMI report](verification/glami_acquisition_20261024.json). Original resolution in this default dataset is approximately 228×298; fine wash details may be inadequate. The earlier zero-result metadata directory is not an image subset. The corrected directory is `glami_jeans_20261024T150212Z`.

Saved privately in [GLAMI acquisition output, version 361844044](https://www.kaggle.com/code/jemincha/denim-atlas-glami-jeans-acquisition/output?scriptVersionId=361844044). The saved viewer reports 313 output files. Preserve the publisher/source card and cite Kosar et al., *GLAMI-1M: A Multilingual Image-Text Fashion Dataset*, BMVC 2022. Unchanged subset images and a derived screening index are recorded; no whole-archive checksum is claimed.

A proposed interruption during the slow range-read phase was rejected by automatic approval review because preservation of in-session progress was not established. It was not bypassed; acquisition continued and completed normally. The public ZIP was not fully downloaded and no whole-archive MD5 verification is claimed. Individual image verification and hashes are recorded.

## DeepFashion application

Sources: [official access instructions](https://mmlab.ie.cuhk.edu.hk/projects/DeepFashion.html), [release agreement](https://mmlab.ie.cuhk.edu.hk/projects/DeepFashion/DeepFashionAgreement.pdf), [In-shop benchmark](https://mmlab.ie.cuhk.edu.hk/projects/DeepFashion/InShopRetrieval.html).

The signed PDF and personal email evidence stay under ignored `data/private/applications/` and the private task artifact directory. Do not copy addresses, signatures or the PDF into committed documentation. Sending a request is not dataset approval or a grant for cloud processing. The request explicitly asks whether private Kaggle/Colab processing is consistent with the terms. The institution account login was verified; an email rejection concerned the official page's old CC address, not the applicant account.

The original request to the official page's primary contact is recorded in Sent. The old CUHK CC returned an address-not-found error. [HKU's current profile](https://datascience.hku.hk/people/ping-luo/) lists the same researcher at a different HKU address; the corrected copy and signed attachment were recorded in Sent. This is one application with a delivery correction, not two approvals. No reply or password was received during this action.

Next after acquisition: visually confirm denim/crops, review duplicate and variant groups, assign disjoint research splits, and build human-judged fixed pools. No source automatically supplies the cross-product appearance judgments required by this study.
