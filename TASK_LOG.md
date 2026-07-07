# Task Log

This file is the handoff document for future Codex sessions across different local machines.

## Current Status

- Repository has been initialized for the VisA supervised defect segmentation project.
- Project direction is fixed as supervised defect segmentation, not broad anomaly localization comparison.
- Local analysis and Colab training roles have been separated.
- Local VisA data is available at `C:/Users/EL010/Documents/datasets/VisA_data` on `local_main_laptop`.
- First EDA pass is complete using `2cls_highshot.csv`.
- A reproducible train/val/test split has been generated at `data/splits/visa_2cls_highshot_train_val_test.csv`.

## Last Completed

- Created initial repository structure.
- Added project context, data guide, environment guide, and experiment plan.
- Added placeholder folders for configs, local analysis scripts, Colab training notebooks, source code, app, and results.
- Implemented local EDA scripts in `analysis/`.
- Confirmed all image and mask paths in `2cls_highshot.csv` exist.
- Generated `results/dataset_distribution.csv`.
- Generated `results/mask_area_by_image.csv` and `results/mask_area_stats.csv`.
- Generated local-only GT overlay samples under `results/figures/gt_overlays/`.
- Created train/val/test split from the official high-shot split.

## Next Tasks

1. Review EDA outputs and decide whether `2cls_highshot` remains the main split.
2. Implement `src/datasets/visa_dataset.py` using `data/splits/visa_2cls_highshot_train_val_test.csv`.
3. Implement baseline metrics and loss functions.
4. Create the first Colab U-Net training notebook.
5. Run a small U-Net 256 smoke test on T4.

## Decisions

- Use `analysis/` for local EDA and data preparation.
- Use `notebooks/` mostly for Colab model training.
- Keep split CSV files in Git under `data/splits/`.
- Do not commit raw VisA data, extracted image folders, checkpoints, or large prediction dumps.
- Use T4 for U-Net baseline and quick validation.
- Use A100 for SegFormer/DeepLabV3+ or final high-resolution training.
- Use `2cls_highshot.csv` rather than `1cls.csv` for supervised segmentation because `1cls.csv` has no anomaly samples in train.
- Use local `train/val/test` split generated from `2cls_highshot.csv` with 20% of official train reserved for validation.
- Keep GT overlay batches local-only and ignored by Git.

## Open Questions

- Final choice between Streamlit and Gradio for the demo app.
- Exact Google Drive path for `VisA.zip`.
- Whether to commit a small curated subset of overlay figures later for README/portfolio.
