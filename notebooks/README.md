# Colab Training Notebooks

Keep this folder focused on model training notebooks.

Local EDA and data analysis should live in `analysis/`.

Planned notebooks:

- `01_train_unet_256_aug_none_colab.ipynb`
- `02_train_unet_256_aug_mild_colab.ipynb`
- `03_train_segformer_colab.ipynb`
- `04_train_final_model_colab.ipynb`

## First Augmentation Comparison

Run these two notebooks first on Colab T4:

```text
01_train_unet_256_aug_none_colab.ipynb
02_train_unet_256_aug_mild_colab.ipynb
```

Optional ablation notebooks:

```text
03_train_unet_256_aug_bc_colab.ipynb
04_train_unet_256_aug_geo_colab.ipynb
```

Augmentation definitions:

```text
aug_none:
  resize only

aug_bc:
  resize
  RandomBrightnessContrast brightness_limit=0.12, contrast_limit=0.12, p=0.5

aug_geo:
  resize
  ShiftScaleRotate shift_limit=0.03, scale_limit=0.08, rotate_limit=10, p=0.5

aug_mild:
  resize
  aug_bc
  aug_geo
```

Current lightweight baseline settings:

```text
EPOCHS = 10
NUM_WORKERS = 0
LOSS_NAME = bce_dice
THRESHOLD = 0.5
```

The notebooks also log diagnostic fields such as `pred_prob_mean`, `pred_prob_max`, `pred_positive_ratio`, and `target_positive_ratio`. These are for interpreting zero Dice cases and do not change the baseline training setup.

Both notebooks save outputs under:

```text
/content/drive/MyDrive/VisA_segmentation/visa_results/colab_runs/{experiment_name}
```

They expect a Drive archive at one of these paths:

```text
/content/drive/MyDrive/VisA_segmentation/VisA.tar
/content/drive/MyDrive/VisA_segmentation/VisA.zip
```

The archive is extracted into `/content/data`, and training uses the local runtime path `/content/data/VisA`.

Share these files back for comparison:

- `final_metrics.csv`
- `val_category_metrics.csv`
- `test_category_metrics.csv`
- `metrics.csv`
- `learning_curves.png`
- `val_prediction_grid.jpg`
- `test_prediction_grid.jpg`
