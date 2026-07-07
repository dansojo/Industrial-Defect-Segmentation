# Practical Vision Checklist

This project should be presented as a practical inspection-system-oriented computer vision project, not only as a model accuracy experiment.

Use this checklist while building the final README, portfolio document, demo, and experiment report.

## 1. Data Leakage Risk

Explain how the split was selected and what leakage risks remain.

Required points:

- Use a fixed split CSV for reproducibility.
- Avoid random split without checking product/category balance.
- Explain that production-lot, camera, or time-based split is not available in the public VisA dataset.
- Confirm category-wise anomaly samples exist in train/validation/test.

Current project decision:

- Main split: `data/splits/visa_2cls_highshot_train_val_test.csv`
- Derived from official `2cls_highshot.csv`.
- Official test split is preserved.
- Official train split is stratified by object and label, with 20% reserved for validation.

## 2. Label Quality Check

Treat mask overlay generation as label QA, not just visualization.

Required outputs:

- GT overlay samples by category.
- A small set of label quality notes.
- Examples of clean masks and ambiguous masks if found.

Suggested categories:

- `good_mask`
- `loose_mask`
- `partial_mask`
- `ambiguous_defect`
- `possible_label_noise`

## 3. Defect Size Distribution

Use mask area analysis to explain model and input-size choices.

Required outputs:

- Per-image defect area ratio CSV.
- Category-wise mask area summary.
- Discussion of small-defect categories.

Current finding:

- `macaroni1` and `macaroni2` have very small median defect area ratios.
- This supports testing higher input sizes such as 384 or 512 and avoiding overly aggressive crop/blur augmentations.

## 4. Category-Wise Difficulty

Do not report only overall metrics.

Required outputs:

- Category-wise Dice.
- Category-wise IoU.
- Category-wise Precision/Recall.
- Category-wise failure examples.

Interpretation should mention:

- Categories with small defects may show low recall.
- Categories with complex normal patterns may show false positives.
- Category-specific thresholding may reduce performance imbalance.

## 5. Augmentation Rationale

Augmentation should be justified as simulated real-world variation, not used blindly.

Before finalizing augmentation, check:

- Image resolution and aspect ratio distribution.
- Brightness and contrast variation.
- Whether product orientation is fixed or variable.
- Whether defects are too small for strong crop or blur.

Likely safe first candidates:

- Resize.
- Mild brightness/contrast.
- Mild shift/scale/rotation.
- Horizontal flip only if product semantics allow it.

Use carefully or defer:

- Strong random crop.
- Vertical flip.
- Large rotation.
- Strong blur.
- Excessive color jitter.

## 6. Threshold Policy

The project should frame thresholding as an inspection policy decision.

Required comparisons:

- Fixed threshold 0.5.
- Validation-best global threshold.
- Category-specific threshold.

Evaluation should discuss:

- Recall-oriented threshold for reducing missed defects.
- Precision-oriented threshold for reducing false alarms.
- Trade-off between missed defects and false alarms.

## 7. Failure Case Taxonomy

Failure analysis must be part of the final output.

Use these categories:

- `small_defect_miss`
- `texture_false_positive`
- `boundary_over_segmentation`
- `boundary_under_segmentation`
- `background_false_positive`
- `category_specific_failure`
- `threshold_sensitive_case`
- `label_ambiguity`

For each selected failure case, save or document:

- Original image.
- Ground-truth mask.
- Predicted mask.
- Overlay.
- Failure category.
- Short explanation.
- Possible improvement.

## 8. Deployment and Operation Constraints

Even though this is a prototype, include practical constraints.

Required points:

- Inference time per image.
- Model size or checkpoint size.
- Input resolution trade-off.
- Threshold used.
- Post-processing used.
- Output fields useful for inspection.

Demo output should include:

- Defect status.
- Predicted mask.
- Overlay.
- Defect area ratio.
- Defect count.
- Bounding boxes.
- Threshold.
- Inference time.

## 9. Experiment Reproducibility

Every experiment should be traceable.

Experiment tables should include:

- `experiment_id`
- `split_file`
- `model`
- `loss`
- `input_size`
- `augmentation`
- `threshold`
- `postprocess`
- `dice`
- `iou`
- `precision`
- `recall`
- `inference_time`
- `checkpoint_path`

## Portfolio Message

Recommended wording:

> This project does not only compare segmentation model accuracy. It treats industrial defect detection as an inspection support problem, checking data leakage risk, label quality, defect size distribution, category-wise behavior, threshold policy, failure cases, and deployment constraints.
