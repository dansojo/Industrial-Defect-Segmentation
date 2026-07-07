"""Inspect the local VisA dataset structure."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from common import add_common_args, resolve_profile


def count_files(path: Path, patterns: tuple[str, ...] = ("*.JPG", "*.jpg", "*.png")) -> int:
    if not path.exists():
        return 0
    return sum(1 for pattern in patterns for _ in path.glob(pattern))


def main() -> None:
    parser = add_common_args("Inspect the VisA dataset structure.")
    args = parser.parse_args()

    profile = resolve_profile(args.profile)
    data_root = profile["data_root"]
    split_path = data_root / "split_csv" / args.split_csv

    if not data_root.exists():
        raise FileNotFoundError(f"Data root does not exist: {data_root}")
    if not split_path.exists():
        raise FileNotFoundError(f"Split CSV does not exist: {split_path}")

    categories = sorted(
        p.name
        for p in data_root.iterdir()
        if p.is_dir() and p.name != "split_csv"
    )
    df = pd.read_csv(split_path)

    rows = []
    for category in categories:
        base = data_root / category / "Data"
        rows.append(
            {
                "object": category,
                "normal_images": count_files(base / "Images" / "Normal"),
                "anomaly_images": count_files(base / "Images" / "Anomaly"),
                "anomaly_masks": count_files(base / "Masks" / "Anomaly", ("*.png", "*.JPG", "*.jpg")),
                "has_image_anno": (data_root / category / "image_anno.csv").exists(),
            }
        )

    summary = pd.DataFrame(rows)
    missing_images = sum(not (data_root / p).exists() for p in df["image"])
    masks = df["mask"].fillna("").astype(str)
    missing_masks = sum((m != "") and not (data_root / m).exists() for m in masks)

    print(f"Data root: {data_root}")
    print(f"Split CSV: {split_path.name}")
    print(f"Categories: {len(categories)}")
    print(summary.to_string(index=False))
    print()
    print("Split summary:")
    print(df.groupby(["split", "label"]).size().unstack(fill_value=0).to_string())
    print()
    print(f"Rows: {len(df)}")
    print(f"Missing image paths: {missing_images}")
    print(f"Non-empty mask paths: {(masks != '').sum()}")
    print(f"Missing mask paths: {missing_masks}")


if __name__ == "__main__":
    main()
