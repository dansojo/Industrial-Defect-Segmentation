# Task Log

This file is the handoff document for future Codex sessions across different local machines.

## Current Status

- Repository has been initialized for the VisA supervised defect segmentation project.
- Project direction is fixed as supervised defect segmentation, not broad anomaly localization comparison.
- Local analysis and Colab training roles have been separated.
- Local VisA data is available at `C:/Users/EL010/Documents/datasets/VisA_data` on `local_main_laptop`.
- First EDA pass is complete using `2cls_highshot.csv`.
- A reproducible train/val/test split has been generated at `data/splits/visa_2cls_highshot_train_val_test.csv`.
- Practical vision engineering checklist has been added and should guide all final deliverables.
- Image-property EDA and sample-grid generation are complete enough to define the first augmentation hypotheses.
- First two Colab notebooks for U-Net 256 augmentation comparison have been created.
- Colab data path is set to `/content/drive/MyDrive/VisA_segmentation/VisA`.

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
- Added `PRACTICAL_VISION_CHECKLIST.md` to preserve the project direction as a practical inspection-system-oriented CV project.
- Added image-property EDA script and generated sampled image statistics.
- Added sample-grid generation script and generated local-only category grids.
- Created `AUGMENTATION_NOTES.md` with first augmentation rationale.
- Implemented reusable baseline code for VisA Dataset, U-Net, BCE+Dice loss, metrics, and prediction visualization.
- Created `notebooks/01_train_unet_256_aug_none_colab.ipynb`.
- Created `notebooks/02_train_unet_256_aug_mild_colab.ipynb`.

## Next Tasks

1. Run `01_train_unet_256_aug_none_colab.ipynb` on Colab T4.
2. Run `02_train_unet_256_aug_mild_colab.ipynb` on Colab T4.
3. Share `final_metrics.csv`, category metrics, learning curves, and prediction grids from both runs.
4. Compare `aug_none` versus `aug_mild` and select the first base augmentation policy.
5. Plan category/group-specific augmentation search based on the comparison.

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
- Treat augmentation choices as hypotheses derived from EDA and validate them through baseline experiments.
- Always include data leakage risk, label quality, category-wise behavior, threshold policy, failure analysis, and deployment constraints in final project outputs.
- First augmentation comparison should be `aug_none` versus `aug_mild` rather than jumping directly to category-specific augmentation.
- Colab result files should be saved under `/content/drive/MyDrive/VisA_segmentation/visa_results/colab_runs/{experiment_name}` and shared back for analysis.

## Known Local Limitations

- `torch` is not installed in the current local Python environment, so Dataset/model runtime checks are expected to run in Colab.
- Source files and notebooks have been syntax-checked locally, but GPU training must be verified in Colab.

## Open Questions

- Final choice between Streamlit and Gradio for the demo app.
- Exact Google Drive path for `VisA.zip`.
- Whether to commit a small curated subset of overlay figures later for README/portfolio.
