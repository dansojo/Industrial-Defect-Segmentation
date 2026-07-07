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

Both notebooks save outputs under:

```text
/content/drive/MyDrive/visa_results/colab_runs/{experiment_name}
```

Share these files back for comparison:

- `final_metrics.csv`
- `val_category_metrics.csv`
- `test_category_metrics.csv`
- `metrics.csv`
- `learning_curves.png`
- `val_prediction_grid.jpg`
- `test_prediction_grid.jpg`
