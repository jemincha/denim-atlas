# Representing denim appearance and defining similarity

October 29, 2026. **Working design, not a frozen label ontology or implemented model.** It follows the [axis-separation audit](AXIS_SEPARATION_AUDIT.md). Existing source labels, packets and model checkpoints are unchanged.

## Representation before aggregation

Keep two comparison axes, each with structured subordinate attributes. Their separation is a task definition, not a claim that the attributes are statistically independent. Preserve familiar retail names as source metadata rather than treating every name as one mutually exclusive class.

- **Fit volume and leg shape differ.** Straight describes a leg profile, while width/volume can vary. Bootcut combines upper-leg and lower-leg properties. Baggy/barrel/tapered names can overlap other properties. The [Levi's guide](https://help.levi.com/hc/en-us/articles/360025097092-Levi-s-Product-Size-Guide) describes fits through multiple regions. Do not encode skinny/slim/straight/wide/bootcut as one linear numerical scale.
- **Black is not merely a darker blue.** Separate photographed color family from lightness, chroma and apparent yellow cast. [CIE's CIELAB definition](https://cie.co.at/eilvterm/17-23-076) separates lightness, chroma and hue. Using image-color coordinates is not calibrated measurement of the original fabric. Apparent yellow cast is neither physical yellow-content percentage nor an inferred lighting temperature in kelvin.
- **Visible fading is not a manufacturing-process label.** [CottonWorks](https://cottonworks.com/learning-hub/denim/denim-finishing/) describes finishing effects that mimic wear patterns. Record visible contrast, coverage, pattern and location; do not identify wear versus finishing from appearance alone. Avoid adding independent “wash strength” and “fading strength” scores for the same visible contrast.

## Initial eight attribute groups

These are proposed recording groups, not eight mandatory manual questions for every image. Missing evidence stays missing. Ordinal bins are anchored by example photos before use; their indices do not imply equal perceptual distances.

| Axis / group | Initial representation | Important boundary |
|---|---|---|
| Silhouette: visible volume | Ordered tight-looking / slim / regular / roomy / very wide | Observed appearance, not actual garment ease, wearer measurements or a universal mapping from retail names |
| Silhouette: leg profile | Tapered / straight / flared / barrel-like / mixed / unknown | Upper, knee and hem shape may require regional notes; bootcut/baggy remain descriptive tags, not extra positions on a volume scale |
| Surface: color family | Blue / near-neutral / other, with ambiguous values left unresolved | Blue-black and faded black require hue/chroma context; the family alone cannot rank all colors |
| Surface: lightness | Dark / medium / light, optionally mixed | Use explicitly observed brightness; preserve named shades separately. Do not derive brightness from a retail color name |
| Surface: apparent yellow cast | Cool-looking / neutral / yellow-warm-looking | Conditioned on the observed image; no white-balance restoration. Brightness and saturation must not silently stand in for warmth |
| Surface: apparent fade contrast | None / weak / medium / strong | The contrast of visible lightened patterns, not average lightness or proof of irreversible change |
| Surface: pattern and placement | Visible whiskers, broad thigh lightening, knee lightening, mottling, seam/hem contrast; region and coarse coverage | Multiple tags allowed. Strong thigh fading and strong knee fading are not equivalent merely because both are “strong” |
| Surface: distressing | Visible rips/fraying, location and coarse extent; absent only when observable | Tiny knee tear and extensive bilateral rips should not share an undifferentiated mismatch penalty |

Readable weave/slub/grain can be added as an optional texture descriptor. Current small catalog images may not resolve these details. Do not infer weight, stretch, roughness to touch or composition. Regional width profiles and continuous color descriptors can refine the coarse groups later; do not fabricate decimal precision now.

## Store observations, not product-wide guesses

Attach attributes to an **image/garment observation**, with its crop/hash and visible regions. Two photos of one product can have different photographed colors. Keep identity groups separate for split protection.

For each attribute retain its value or unknown, observability reason, relevant region, source (human / source-title proxy / unverified machine), and annotation/rubric version. No model self-confidence is promoted to a calibrated probability. Source-title `straight` is not automatically a human-observed leg profile. Unknown is not “none,” a negative label, or perfect agreement.

The expansion audit explicitly includes mid-blue/light, light-blue/medium and dark-blue/medium responses. This corrects the initial suggestion that familiar light/mid/dark blue names could be derived directly from photographed brightness. Keep the original color description and the separately supplied lightness; do not overwrite either to force agreement or assume an extra saturation/indigo-depth label that was not measured.

Compare only mutually readable corresponding evidence. A back view does not establish absent front whiskers. If surface is readable but silhouette is cropped, surface retrieval remains meaningful; full two-axis acceptability is unestablished. A candidate with fewer readable attributes must not receive an artificially perfect distance after dropping every difficult field. Report coverage and limit the claim.

## What “similar” means

Return separate silhouette and surface comparisons first. Nearby ordinal labels can be closer than distant labels; categorical labels do not have meaningful integer subtraction. Matching broad labels is helpful evidence, not a sufficient positive label: two medium-blue straight jeans can still differ strongly in local patterns.

The proposed model retains FashionSigLIP and adds explicit axis-conditioned distances, initially two small heads rather than a different model for every attribute. Structured attributes provide sparse auxiliary supervision and interpretable checks; learned visual features retain within-bin detail. Geometry and surface detail may require different regions/scales. A head cannot recover unreadable texture from low-resolution input. None of these heads has been trained yet.

For a full-appearance ranking, propose a **non-compensating development policy**: a large mismatch on either main axis should not disappear behind a high score on the other. Calibrate each axis distance by a development-set tolerance, then rank by the larger normalized mismatch. Declare a close two-axis match only when both meet their respective tolerances and observation coverage is adequate. This is a proposed ranking/acceptance rule, not an automatic conversion of the two human grades into a new grade. If nothing qualifies, nearest candidates remain nearest; do not claim they are close matches.

No weights, tolerances or equivalence between ordinal steps are fixed yet. Calibrate on development examples, preserve axis reports, and test a frozen rule on fresh product groups. Overall human acceptability, if collected, stays a directly judged separate target. Similarity is graded and need not be transitive; do not force every image into one “similar-product cluster.”

## Supervision and next experiment

Collect reusable observation attributes where evidence is reliable, rather than an all-pairs grid. Only request a small number of axis-specific comparisons for uncertain relationships and to calibrate ordinal boundaries. Include the four contrasts: similar silhouette/similar surface, similar silhouette/different surface, different silhouette/similar surface, and different/different. Do not assign these cells solely from source names or unverified VLM descriptions.

Positive/negative relationships must name the target axis. A same-cut/different-color pair can be a silhouette-positive and surface-negative when those observations are verified. Missing labels do not enter that axis loss. Freeze identity/duplicate groups before mining; anchor photo selection and tolerance fitting use development material only. Existing overall labels remain overall labels.

Report silhouette and surface retrieval separately using independently judged pools, with unknown coverage and relevant regional errors. Then check joint acceptability without averaging away a failing axis. The immediate gate is reliable attributes and contrast examples, not a larger fit-only run or a promise that this ontology improves retrieval.

This design adapts attribute-conditioned similarity principles from [ASEN](https://arxiv.org/abs/2002.02814) and [Conditional Similarity Networks](https://openaccess.thecvf.com/content_cvpr_2017/papers/Veit_Conditional_Similarity_Networks_CVPR_2017_paper.pdf). Those papers support distinct similarity notions; they do not validate this denim taxonomy, proposed aggregation rule or our model's performance.
