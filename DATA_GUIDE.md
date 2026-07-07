# Data Guide

## Dataset

Main dataset: VisA (Visual Anomaly Dataset)

The original VisA dataset should not be committed to this repository. Keep only documentation, scripts, and split CSV files in Git.

## Expected Data Sources

Local machines can use different absolute paths. Use environment profile names rather than hard-coding one path everywhere.

Recommended profiles:

- `local_main_laptop`
- `local_home_laptop`
- `local_desktop`
- `colab_t4`
- `colab_a100`

## Colab Data Plan

Recommended Google Drive layout:

```text
/content/drive/MyDrive/datasets/VisA.zip
/content/drive/MyDrive/visa_results/
```

Recommended Colab runtime layout:

```text
/content/repo/Industrial-Defect-Segmentation
/content/data/VisA
/content/drive/MyDrive/visa_results
```

For training, unzip the dataset into `/content/data/VisA` instead of reading image files directly from Google Drive. This should reduce I/O overhead.

## Repository Data Policy

Commit:

- `data/README.md`
- `data/splits/*.csv`
- small metadata summaries
- selected small result tables

Do not commit:

- raw VisA image folders
- extracted dataset archives
- model checkpoints
- full prediction dumps
- large overlay batches

## Split Policy

Train/validation/test splits should be generated locally and committed as CSV files under:

```text
data/splits/
```

The same split files should be used in local evaluation and Colab training so experiments remain comparable.

Current main split:

```text
data/splits/visa_2cls_highshot_train_val_test.csv
```

This split is derived from the official `split_csv/2cls_highshot.csv`. The official train split is stratified by object and label, then 20% is reserved as validation. The official test split is kept unchanged.

Current totals:

```text
train: 576 anomaly, 4619 normal
val:   144 anomaly, 1154 normal
test:  480 anomaly, 3848 normal
```
