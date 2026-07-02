# Industrial Defect Segmentation

VisA dataset based supervised defect segmentation project for industrial quality inspection.

The project focuses on pixel-level defect segmentation rather than anomaly localization model comparison. The final goal is to train and compare segmentation models, analyze category-wise performance, tune thresholds, apply post-processing, and build a lightweight inspection demo that reports masks, overlays, defect area, defect count, and bounding boxes.

## Scope

- Dataset: VisA (Visual Anomaly Dataset)
- Task: supervised binary defect segmentation
- Main metrics: Dice, IoU, Precision, Recall, F1-score, inference time
- Local work: EDA, dataset inspection, split generation, result analysis, documentation
- Colab work: model training and heavier evaluation on T4/A100
- Excluded: main object detection project, broad anomaly localization model comparison

## Repository Layout

```text
configs/      Environment paths and experiment configs
data/         Dataset notes and versioned split CSVs only
analysis/     Local CPU scripts for EDA and dataset preparation
notebooks/    Colab notebooks for model training
src/          Reusable dataset, model, loss, metric, visualization code
app/          Streamlit or Gradio demo
results/      Lightweight result tables and selected figures
```

Large files such as raw images, extracted datasets, checkpoints, and full prediction dumps should not be committed. See `DATA_GUIDE.md` and `ENV_GUIDE.md`.

## Current Workflow

1. Prepare VisA locally or in Google Drive.
2. Run local EDA and split generation from `analysis/`.
3. Train models in Colab notebooks under `notebooks/`.
4. Save experiment metrics to CSV and selected figures to `results/`.
5. Update `TASK_LOG.md` after each work session so another local Codex session can continue.

## First Models

- U-Net 256 BCE baseline
- U-Net 256 BCE + Dice
- SegFormer-B0 384 or 512 on A100 when available
- DeepLabV3+ as optional comparison
