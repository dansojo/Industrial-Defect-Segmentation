"""Analyze image size, aspect ratio, brightness, contrast, and RGB statistics."""

from __future__ import annotations

import cv2
import pandas as pd

from common import add_common_args, ensure_output_dir, resolve_profile


def image_stats(image_path):
    image_bgr = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if image_bgr is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    height, width = image_rgb.shape[:2]

    return {
        "height": height,
        "width": width,
        "aspect_ratio": width / height,
        "mean_r": float(image_rgb[:, :, 0].mean()),
        "mean_g": float(image_rgb[:, :, 1].mean()),
        "mean_b": float(image_rgb[:, :, 2].mean()),
        "brightness_mean": float(gray.mean()),
        "brightness_std": float(gray.std()),
        "contrast": float(gray.std()),
    }


def main() -> None:
    parser = add_common_args("Analyze image properties for augmentation planning.")
    parser.add_argument(
        "--samples-per-object-label",
        type=int,
        default=200,
        help="Balanced sample count per object/label. Use 0 to process every image.",
    )
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    profile = resolve_profile(args.profile)
    data_root = profile["data_root"]
    output_root = ensure_output_dir(profile["output_root"])

    df = pd.read_csv(data_root / "split_csv" / args.split_csv)
    if args.samples_per_object_label > 0:
        parts = []
        for _, group in df.groupby(["object", "label"], sort=False):
            parts.append(
                group.sample(
                    n=min(args.samples_per_object_label, len(group)),
                    random_state=args.seed,
                )
            )
        df = pd.concat(parts, ignore_index=True)
        print(f"Using balanced sample rows: {len(df)}")
    rows = []
    for _, row in df.iterrows():
        stats = image_stats(data_root / row["image"])
        rows.append(
            {
                "object": row["object"],
                "split": row["split"],
                "label": row["label"],
                "image": row["image"],
                **stats,
            }
        )

    props = pd.DataFrame(rows)
    props_path = output_root / "image_properties.csv"
    props.to_csv(props_path, index=False)

    category_stats = (
        props.groupby(["object", "label"])
        .agg(
            count=("image", "count"),
            width_min=("width", "min"),
            width_median=("width", "median"),
            width_max=("width", "max"),
            height_min=("height", "min"),
            height_median=("height", "median"),
            height_max=("height", "max"),
            aspect_median=("aspect_ratio", "median"),
            brightness_mean=("brightness_mean", "mean"),
            brightness_std_mean=("brightness_std", "mean"),
            contrast_mean=("contrast", "mean"),
        )
        .reset_index()
        .sort_values(["object", "label"])
    )
    stats_path = output_root / "image_property_stats.csv"
    category_stats.to_csv(stats_path, index=False)

    label_diff = (
        props.pivot_table(
            index="object",
            columns="label",
            values=["brightness_mean", "contrast"],
            aggfunc="mean",
        )
        .reset_index()
    )
    label_diff.columns = [
        "_".join(str(part) for part in col if part).strip("_")
        if isinstance(col, tuple)
        else col
        for col in label_diff.columns
    ]
    if {"brightness_mean_anomaly", "brightness_mean_normal"}.issubset(label_diff.columns):
        label_diff["brightness_anomaly_minus_normal"] = (
            label_diff["brightness_mean_anomaly"] - label_diff["brightness_mean_normal"]
        )
    if {"contrast_anomaly", "contrast_normal"}.issubset(label_diff.columns):
        label_diff["contrast_anomaly_minus_normal"] = (
            label_diff["contrast_anomaly"] - label_diff["contrast_normal"]
        )

    diff_path = output_root / "image_property_label_diff.csv"
    label_diff.to_csv(diff_path, index=False)

    print(category_stats.to_string(index=False))
    print(f"\nSaved: {props_path}")
    print(f"Saved: {stats_path}")
    print(f"Saved: {diff_path}")


if __name__ == "__main__":
    main()
