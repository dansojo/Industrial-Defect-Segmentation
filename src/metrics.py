"""Segmentation metrics: Dice, IoU, Precision, Recall, F1."""

from __future__ import annotations

import torch


def binary_stats(
    logits: torch.Tensor,
    targets: torch.Tensor,
    threshold: float = 0.5,
) -> dict[str, float]:
    probs = torch.sigmoid(logits)
    preds = probs >= threshold
    targets_bool = targets >= 0.5

    tp = (preds & targets_bool).sum().item()
    fp = (preds & ~targets_bool).sum().item()
    fn = (~preds & targets_bool).sum().item()
    tn = (~preds & ~targets_bool).sum().item()
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn}


def metrics_from_stats(stats: dict[str, float], eps: float = 1e-7) -> dict[str, float]:
    tp = stats["tp"]
    fp = stats["fp"]
    fn = stats["fn"]
    precision = tp / (tp + fp + eps)
    recall = tp / (tp + fn + eps)
    dice = (2 * tp) / (2 * tp + fp + fn + eps)
    iou = tp / (tp + fp + fn + eps)
    f1 = 2 * precision * recall / (precision + recall + eps)
    return {
        "dice": dice,
        "iou": iou,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def merge_stats(items: list[dict[str, float]]) -> dict[str, float]:
    total = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}
    for item in items:
        for key in total:
            total[key] += item[key]
    return total
