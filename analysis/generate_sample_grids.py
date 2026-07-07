"""Generate sample image grids for category-wise visual EDA."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
import pandas as pd

from common import add_common_args, ensure_output_dir, resolve_profile


def read_rgb(path: Path):
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def resize_to_tile(image, tile_size: int):
    height, width = image.shape[:2]
    scale = min(tile_size / width, tile_size / height)
    new_width = max(1, int(width * scale))
    new_height = max(1, int(height * scale))
    resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    canvas = np.full((tile_size, tile_size, 3), 245, dtype=np.uint8)
    y0 = (tile_size - new_height) // 2
    x0 = (tile_size - new_width) // 2
    canvas[y0 : y0 + new_height, x0 : x0 + new_width] = resized
    return canvas


def save_grid(images, out_path: Path, cols: int, tile_size: int):
    rows = int(np.ceil(len(images) / cols))
    canvas = np.full((rows * tile_size, cols * tile_size, 3), 245, dtype=np.uint8)
    for idx, image in enumerate(images):
        row = idx // cols
        col = idx % cols
        tile = resize_to_tile(image, tile_size)
        canvas[row * tile_size : (row + 1) * tile_size, col * tile_size : (col + 1) * tile_size] = tile
    out_bgr = cv2.cvtColor(canvas, cv2.COLOR_RGB2BGR)
    cv2.imwrite(str(out_path), out_bgr)


def main() -> None:
    parser = add_common_args("Generate category-wise sample grids.")
    parser.add_argument("--samples-per-label", type=int, default=12)
    parser.add_argument("--tile-size", type=int, default=180)
    parser.add_argument("--cols", type=int, default=4)
    args = parser.parse_args()

    profile = resolve_profile(args.profile)
    data_root = profile["data_root"]
    output_dir = ensure_output_dir(profile["output_root"] / "figures" / "sample_grids")

    df = pd.read_csv(data_root / "split_csv" / args.split_csv)
    saved = []
    for object_name, object_df in df.groupby("object"):
        for label, label_df in object_df.groupby("label"):
            sample = label_df.sample(
                n=min(args.samples_per_label, len(label_df)),
                random_state=42,
            )
            images = [read_rgb(data_root / row.image) for row in sample.itertuples(index=False)]
            out_path = output_dir / f"{object_name}_{label}_grid.jpg"
            save_grid(images, out_path, cols=args.cols, tile_size=args.tile_size)
            saved.append(out_path)

    mask_area_path = profile["output_root"] / "mask_area_by_image.csv"
    if mask_area_path.exists():
        area_df = pd.read_csv(mask_area_path)
        for object_name, object_df in area_df.groupby("object"):
            sorted_df = object_df.sort_values("defect_area_ratio")
            buckets = {
                "small": sorted_df.head(args.samples_per_label),
                "large": sorted_df.tail(args.samples_per_label),
            }
            mid_start = max(0, len(sorted_df) // 2 - args.samples_per_label // 2)
            buckets["medium"] = sorted_df.iloc[mid_start : mid_start + args.samples_per_label]
            for bucket_name, bucket_df in buckets.items():
                images = [read_rgb(data_root / row.image) for row in bucket_df.itertuples(index=False)]
                out_path = output_dir / f"{object_name}_anomaly_{bucket_name}_defects_grid.jpg"
                save_grid(images, out_path, cols=args.cols, tile_size=args.tile_size)
                saved.append(out_path)

    print(f"Saved {len(saved)} grids to {output_dir}")


if __name__ == "__main__":
    main()
