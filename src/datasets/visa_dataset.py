"""PyTorch Dataset implementation for VisA defect segmentation."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset


class VisASegmentationDataset(Dataset):
    """Read VisA images and binary masks from a split CSV.

    Normal samples do not have mask paths in VisA. For those rows this dataset
    returns an all-zero mask with the same height and width as the image.
    """

    def __init__(
        self,
        data_root: str | Path,
        split_csv: str | Path,
        split: str,
        transform=None,
    ) -> None:
        self.data_root = Path(data_root)
        self.split_csv = Path(split_csv)
        self.split = split
        self.transform = transform

        df = pd.read_csv(self.split_csv)
        if split not in set(df["split"]):
            available = ", ".join(sorted(df["split"].unique()))
            raise ValueError(f"Unknown split '{split}'. Available splits: {available}")
        self.df = df[df["split"] == split].reset_index(drop=True)

    def __len__(self) -> int:
        return len(self.df)

    def __getitem__(self, index: int):
        row = self.df.iloc[index]
        image_path = self.data_root / row["image"]
        image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
        if image is None:
            raise FileNotFoundError(f"Could not read image: {image_path}")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        mask_value = row.get("mask", "")
        if pd.isna(mask_value) or mask_value == "":
            mask = np.zeros(image.shape[:2], dtype=np.uint8)
        else:
            mask_path = self.data_root / str(mask_value)
            mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
            if mask is None:
                raise FileNotFoundError(f"Could not read mask: {mask_path}")
            mask = (mask > 0).astype(np.uint8)

        if self.transform is not None:
            transformed = self.transform(image=image, mask=mask)
            image = transformed["image"]
            mask = transformed["mask"]
        else:
            image = torch.from_numpy(image.transpose(2, 0, 1)).float() / 255.0
            mask = torch.from_numpy(mask).float()

        if not torch.is_tensor(mask):
            mask = torch.from_numpy(mask).float()
        if mask.ndim == 2:
            mask = mask.unsqueeze(0)
        else:
            mask = mask.float()

        return {
            "image": image.float(),
            "mask": mask.float(),
            "object": row["object"],
            "label": row["label"],
            "image_path": row["image"],
            "mask_path": "" if pd.isna(mask_value) else str(mask_value),
        }
