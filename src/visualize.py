"""Visualization utilities for masks, overlays, and bounding boxes."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
import torch


IMAGENET_MEAN = np.array([0.485, 0.456, 0.406])
IMAGENET_STD = np.array([0.229, 0.224, 0.225])


def tensor_to_rgb(image: torch.Tensor) -> np.ndarray:
    image_np = image.detach().cpu().float().numpy().transpose(1, 2, 0)
    image_np = (image_np * IMAGENET_STD + IMAGENET_MEAN).clip(0, 1)
    return (image_np * 255).astype(np.uint8)


def overlay_mask(image_rgb: np.ndarray, mask: np.ndarray, color=(255, 0, 0), alpha: float = 0.45) -> np.ndarray:
    overlay = image_rgb.copy()
    color_layer = np.zeros_like(image_rgb)
    color_layer[:, :] = np.array(color, dtype=np.uint8)
    mask_bool = mask > 0
    overlay[mask_bool] = (
        (1 - alpha) * image_rgb[mask_bool] + alpha * color_layer[mask_bool]
    ).astype(np.uint8)
    return overlay


def save_prediction_grid(batch, logits: torch.Tensor, output_path: str | Path, max_items: int = 8) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    probs = torch.sigmoid(logits).detach().cpu()
    count = min(max_items, probs.shape[0])
    tiles = []
    for idx in range(count):
        image_rgb = tensor_to_rgb(batch["image"][idx])
        gt_mask = batch["mask"][idx, 0].detach().cpu().numpy() > 0.5
        pred_mask = probs[idx, 0].numpy() >= 0.5
        gt_overlay = overlay_mask(image_rgb, gt_mask, color=(0, 255, 0), alpha=0.45)
        pred_overlay = overlay_mask(image_rgb, pred_mask, color=(255, 0, 0), alpha=0.45)
        tile = np.concatenate([image_rgb, gt_overlay, pred_overlay], axis=1)
        tiles.append(tile)

    grid = np.concatenate(tiles, axis=0)
    cv2.imwrite(str(output_path), cv2.cvtColor(grid, cv2.COLOR_RGB2BGR))
