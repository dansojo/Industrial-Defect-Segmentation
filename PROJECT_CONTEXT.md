# Project Context

## Project Name

Industrial Defect Segmentation

## Goal

Build a supervised defect segmentation project using the VisA dataset. The project should detect defect regions as pixel-level masks and provide useful inspection outputs such as overlay images, defect area ratio, defect count, bounding boxes, and inference time.

## Core Direction

This is not a broad anomaly localization model comparison project. The main direction is supervised semantic segmentation for industrial defect inspection.

The project should answer:

- Can a segmentation model identify where defects are and how large they are?
- Is one global threshold stable across product categories?
- Do category-specific thresholds reduce false positives or false negatives?
- Which model, loss, input size, and post-processing setup gives the best practical balance?

## Dataset

- Main dataset: VisA (Visual Anomaly Dataset)
- Source repository: https://github.com/amazon-science/spot-diff
- Data is not committed to this repository.
- Split CSVs can be committed under `data/splits/`.

## Work Distribution

Local machines:

- Dataset inspection
- EDA
- Split generation
- Result review
- README and portfolio writing
- Demo development

Google Colab:

- Model training
- Heavy model comparison
- Final model training
- Batch inference when useful

## Environment Profiles

Use profile names to describe machine-specific paths:

- `local_main_laptop`
- `local_home_laptop`
- `local_desktop`
- `colab_t4`
- `colab_a100`

Real local paths should be stored in ignored local config files, not hard-coded into source files.

## Important Decisions

- EDA and data analysis should stay outside `notebooks/` when possible.
- `notebooks/` is reserved mostly for Colab model training.
- Reusable code belongs in `src/`.
- Large raw data and checkpoints are excluded from Git.
- T4 is for lightweight experiments and pipeline validation.
- A100 is for heavier candidate training and final runs.
