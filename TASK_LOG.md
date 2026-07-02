# Task Log

This file is the handoff document for future Codex sessions across different local machines.

## Current Status

- Repository has been initialized for the VisA supervised defect segmentation project.
- Project direction is fixed as supervised defect segmentation, not broad anomaly localization comparison.
- Local analysis and Colab training roles have been separated.

## Last Completed

- Created initial repository structure.
- Added project context, data guide, environment guide, and experiment plan.
- Added placeholder folders for configs, local analysis scripts, Colab training notebooks, source code, app, and results.

## Next Tasks

1. Fill machine-specific path config from `configs/paths.example.yaml`.
2. Download or locate VisA dataset for `local_main_laptop`.
3. Implement `analysis/inspect_dataset.py`.
4. Implement `analysis/analyze_distribution.py`.
5. Implement `analysis/generate_gt_overlays.py`.
6. Implement `analysis/make_splits.py`.
7. Create the first Colab U-Net training notebook.

## Decisions

- Use `analysis/` for local EDA and data preparation.
- Use `notebooks/` mostly for Colab model training.
- Keep split CSV files in Git under `data/splits/`.
- Do not commit raw VisA data, extracted image folders, checkpoints, or large prediction dumps.
- Use T4 for U-Net baseline and quick validation.
- Use A100 for SegFormer/DeepLabV3+ or final high-resolution training.

## Open Questions

- Exact local path for VisA on `local_main_laptop`.
- Exact Google Drive path for `VisA.zip`.
- Final choice between Streamlit and Gradio for the demo app.
