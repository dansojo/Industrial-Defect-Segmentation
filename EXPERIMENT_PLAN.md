# Experiment Plan

## Priority 0: Pipeline

- Confirm VisA folder structure.
- Generate stable train/validation/test split CSVs.
- Implement Dataset class.
- Confirm metrics, checkpoint save/load, and visualization.

## Priority 1: Baseline

| Experiment | Model | Loss | Input Size | Threshold | Purpose |
| --- | --- | --- | ---: | --- | --- |
| B0 | U-Net | BCE | 256 | 0.5 | Fast baseline and pipeline validation |
| B1 | U-Net | BCE + Dice | 256 | 0.5 | Check overlap-aware loss improvement |
| B2 | U-Net | BCE + Dice | 256 | val-best | Validate threshold tuning effect |

## Priority 2: Model Comparison

| Experiment | Model | Loss | Input Size | GPU | Purpose |
| --- | --- | --- | ---: | --- | --- |
| M0 | U-Net | BCE + Dice | 384 | T4/A100 | Resolution improvement check |
| M1 | SegFormer-B0 | BCE + Dice or Focal + Dice | 384 | A100 preferred | Lightweight transformer comparison |
| M2 | DeepLabV3+ | BCE + Dice | 384 | A100 preferred | Multi-scale CNN comparison |

## Priority 3: Practical Improvement

- EDA-driven augmentation policy selection.
- Product/group-specific augmentation candidate search.
- Global threshold versus validation-best threshold.
- Category-specific threshold.
- Small object removal.
- Morphological opening/closing.
- Connected component analysis for defect count, area, and bounding boxes.

## Augmentation Experiment Stages

| Stage | Purpose | Epochs | Notes |
| --- | --- | ---: | --- |
| Stage 1 | Compare `aug_none` vs `aug_mild` | 15 | First base augmentation decision |
| Stage 2 | Product/group-specific candidate search | 10 | Efficient screening based on selected base augmentation |
| Stage 3 | Product/group-specific final check | 15 | Confirm top candidate policies before defining `selected_aug_v1` |

The final selected augmentation policy from Stage 3 should be used as the fixed augmentation baseline for later model, loss, input-size, threshold, and post-processing experiments unless later results justify revisiting it.

## Required Result Tables

- `results/experiment_table.csv`
- `results/category_metrics.csv`
- `results/threshold_sweep.csv`

## Final Selection Criteria

- Dice and IoU
- Precision/Recall balance
- Category-wise stability
- Threshold sensitivity
- Inference time
- Visual mask quality
