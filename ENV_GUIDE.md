# Environment Guide

## Profiles

Use profile names to make work portable across machines:

```text
local_main_laptop
local_home_laptop
local_desktop
colab_t4
colab_a100
```

Start from `configs/paths.example.yaml` and create a machine-specific ignored file if needed:

```text
configs/paths.local.yaml
```

## Local Workflow

Local machines are used for CPU-friendly work:

```powershell
python analysis/inspect_dataset.py --profile local_main_laptop
python analysis/analyze_distribution.py --profile local_main_laptop
python analysis/analyze_mask_area.py --profile local_main_laptop
python analysis/generate_gt_overlays.py --profile local_main_laptop
python analysis/make_splits.py --profile local_main_laptop
```

## Colab Workflow

Colab notebooks should follow this pattern:

```text
1. Mount Google Drive.
2. Clone or pull this repository.
3. Install requirements.
4. Copy `/content/drive/MyDrive/VisA_segmentation/VisA` to `/content/data/VisA` or unzip `/content/drive/MyDrive/VisA_segmentation/VisA.zip`.
5. Select experiment config.
6. Train model.
7. Save checkpoints and result CSVs to Google Drive.
8. Commit only lightweight metrics/figures back to Git.
```

## GPU Usage Strategy

T4:

- U-Net 256 baseline
- loss comparison smoke tests
- pipeline validation
- threshold sweep and lightweight evaluation

A100:

- SegFormer-B0 384/512
- DeepLabV3+ 384/512 if included
- final model training
- batch inference for final result images
