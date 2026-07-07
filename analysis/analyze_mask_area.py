"""Analyze defect mask area ratios by category."""

from __future__ import annotations

import cv2
import pandas as pd

from common import add_common_args, ensure_output_dir, resolve_profile


def main() -> None:
    parser = add_common_args("Analyze anomaly mask area ratios by category.")
    args = parser.parse_args()

    profile = resolve_profile(args.profile)
    data_root = profile["data_root"]
    output_root = ensure_output_dir(profile["output_root"])

    df = pd.read_csv(data_root / "split_csv" / args.split_csv)
    anomaly_df = df[df["mask"].notna() & (df["mask"] != "")].copy()

    rows = []
    for row in anomaly_df.itertuples(index=False):
        mask_path = data_root / row.mask
        mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
        if mask is None:
            raise FileNotFoundError(f"Could not read mask: {mask_path}")
        defect_pixels = int((mask > 0).sum())
        total_pixels = int(mask.shape[0] * mask.shape[1])
        rows.append(
            {
                "object": row.object,
                "split": row.split,
                "image": row.image,
                "mask": row.mask,
                "mask_height": mask.shape[0],
                "mask_width": mask.shape[1],
                "defect_pixels": defect_pixels,
                "total_pixels": total_pixels,
                "defect_area_ratio": defect_pixels / total_pixels,
            }
        )

    area_df = pd.DataFrame(rows)
    area_path = output_root / "mask_area_by_image.csv"
    stats_path = output_root / "mask_area_stats.csv"
    area_df.to_csv(area_path, index=False)

    stats = (
        area_df.groupby("object")["defect_area_ratio"]
        .agg(["count", "mean", "median", "min", "max"])
        .reset_index()
        .sort_values("median")
    )
    stats.to_csv(stats_path, index=False)

    print(stats.to_string(index=False))
    print(f"\nSaved: {area_path}")
    print(f"Saved: {stats_path}")


if __name__ == "__main__":
    main()
