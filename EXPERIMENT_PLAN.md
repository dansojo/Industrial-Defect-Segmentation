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

- Global threshold versus validation-best threshold.
- Category-specific threshold.
- Small object removal.
- Morphological opening/closing.
- Connected component analysis for defect count, area, and bounding boxes.

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
