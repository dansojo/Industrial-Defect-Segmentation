# Augmentation Notes

This document records augmentation decisions as hypotheses derived from EDA. Augmentation is not treated as a fixed recipe; it should be validated through baseline experiments and failure analysis.

## Current Status

- First structural EDA is complete.
- Mask area analysis shows strong category differences in defect size.
- Image-property EDA has been run with a balanced sample of up to 200 images per object/label.
- Category-wise sample grids have been generated locally under `results/figures/sample_grids/`.

## Confirmed EDA Findings

- `2cls_highshot.csv` is the main supervised split source.
- `1cls.csv` is not suitable for supervised segmentation training because train has no anomaly samples.
- `macaroni1` and `macaroni2` have very small median defect area ratios.
- GT overlay samples align correctly for inspected samples.
- Each object category has a fixed image resolution internally, but image size and aspect ratio differ across categories.
- Aspect ratio ranges from about 1.08 (`cashew`) to 1.63 (`pcb3`).
- Brightness differs strongly across categories, from very dark `pipe_fryum` to bright `capsules` and `pcb1`.
- Normal/anomaly brightness can differ by category, but this should not be treated as a defect cue because it may reflect dataset capture variation.

## Image-Property EDA Outputs

- `results/image_properties.csv`
- `results/image_property_stats.csv`
- `results/image_property_label_diff.csv`

The current property CSV is based on balanced sampling, not a full-dataset pass. This is sufficient for augmentation planning, but full-dataset statistics can be generated later if needed.

## Augmentation Principles

- Use augmentation to simulate plausible production variation.
- Avoid transformations that can erase tiny defects.
- Avoid transformations that create product orientations unlikely to occur in inspection.
- Start with a mild common augmentation baseline before category-specific augmentation.

## Likely First Baseline

Candidate augmentations:

- Resize to model input size.
- Mild brightness/contrast to simulate lighting variation.
- Mild shift/scale/rotation to simulate small camera or product placement variation.
- Horizontal flip only if visual review suggests product semantics allow it.
- Normalize consistently across all categories.

Use carefully or defer:

- Strong random crop.
- Vertical flip.
- Large rotation.
- Strong blur.
- Excessive color jitter.
- Category-specific augmentation in the first baseline.

## First Experiment Recommendation

Start with two augmentation configs rather than overfitting the plan before training:

```text
aug_none:
  resize only

aug_mild:
  resize
  mild brightness/contrast
  mild shift/scale/rotation
```

Compare `aug_none` and `aug_mild` on U-Net 256 first. Add stronger or category-specific augmentation only after failure-case review.

Optional ablations are prepared in case the combined result needs explanation:

```text
aug_bc:
  resize
  mild brightness/contrast only

aug_geo:
  resize
  mild shift/scale/rotation only
```

## Current Augmentation Parameters

| Transform | Parameter | Value | Interpretation |
| --- | --- | ---: | --- |
| Resize | `height`, `width` | 256, 256 | Baseline input size; simple but may distort aspect ratio |
| RandomBrightnessContrast | `brightness_limit` | 0.12 | Conservative to mild photometric change |
| RandomBrightnessContrast | `contrast_limit` | 0.12 | Conservative to mild contrast change |
| RandomBrightnessContrast | `p` | 0.5 | Common probability; applied to about half of training samples |
| ShiftScaleRotate | `shift_limit` | 0.03 | Conservative translation, up to about 3% of image size |
| ShiftScaleRotate | `scale_limit` | 0.08 | Mild scale change, roughly +/-8% |
| ShiftScaleRotate | `rotate_limit` | 10 | Conservative rotation for inspection images |
| ShiftScaleRotate | `p` | 0.5 | Common probability; applied to about half of training samples |

Overall, these settings are intentionally conservative for defect segmentation. They are weaker than many generic image-classification augmentation recipes because small defects can be erased or displaced by aggressive crop, blur, scale, or rotation.

## Product-Wise Notes

Initial notes based on mask area analysis, sampled image-property statistics, and local sample-grid review.

| Object | Visual Notes | Risk | Candidate Augmentation | Avoid / Use Carefully |
| --- | --- | --- | --- | --- |
| candle | High contrast, simple object appearance | Boundary/lighting sensitivity | Mild brightness/contrast, mild shift | Strong color jitter |
| capsules | Many small capsules with varied orientations | Object layout variation, specular highlights | Mild brightness/contrast, mild shift | Strong crop, strong blur |
| cashew | Darker scene, natural shape variation | Boundary variation, lighting variation | Mild rotation/scale, brightness/contrast | Large crop |
| chewinggum | High contrast and textured object/background | Texture false positives | Mild brightness/contrast | Strong blur |
| fryum | Bright wide-aspect images | Shape/placement variation | Mild rotation/scale | Strong crop |
| macaroni1 | Very small defect area distribution | Small-defect miss | Higher input size, mild photometric aug | Strong crop/blur |
| macaroni2 | Very small defect area distribution | Small-defect miss | Higher input size, mild photometric aug | Strong crop/blur |
| pcb1 | Complex normal PCB pattern | Texture/component false positives | Mild brightness/contrast | Strong blur, large rotation |
| pcb2 | Complex normal PCB pattern, anomaly brighter on average | Texture/component false positives | Mild brightness/contrast | Treat brightness as defect cue |
| pcb3 | Widest aspect ratio among categories | Distortion from square resize | Resize experiment, possible padding later | Aggressive crop |
| pcb4 | Darker PCB category | Lighting sensitivity, texture false positives | Mild brightness/contrast | Strong blur |
| pipe_fryum | Very dark category | Low-light sensitivity | Mild brightness/contrast | Excessive brightness shift |
