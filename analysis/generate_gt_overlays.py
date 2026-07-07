"""Generate local ground-truth mask overlay samples."""

from __future__ import annotations

import cv2
import pandas as pd

from common import add_common_args, ensure_output_dir, resolve_profile


def make_overlay(image, mask, alpha: float = 0.45):
    overlay = image.copy()
    red = image.copy()
    red[:, :, 2] = 255
    red[:, :, 1] = (red[:, :, 1] * 0.25).astype(red.dtype)
    red[:, :, 0] = (red[:, :, 0] * 0.25).astype(red.dtype)
    mask_bool = mask > 0
    overlay[mask_bool] = cv2.addWeighted(image, 1 - alpha, red, alpha, 0)[mask_bool]
    return overlay


def main() -> None:
    parser = add_common_args("Generate GT mask overlay samples.")
    parser.add_argument("--samples-per-object", type=int, default=5)
    args = parser.parse_args()

    profile = resolve_profile(args.profile)
    data_root = profile["data_root"]
    output_dir = ensure_output_dir(profile["output_root"] / "figures" / "gt_overlays")

    df = pd.read_csv(data_root / "split_csv" / args.split_csv)
    anomaly_df = df[df["mask"].notna() & (df["mask"] != "")].copy()

    saved = []
    for object_name, group in anomaly_df.groupby("object"):
        sample = group.head(args.samples_per_object)
        object_dir = ensure_output_dir(output_dir / object_name)
        for row in sample.itertuples(index=False):
            image = cv2.imread(str(data_root / row.image), cv2.IMREAD_COLOR)
            mask = cv2.imread(str(data_root / row.mask), cv2.IMREAD_GRAYSCALE)
            if image is None or mask is None:
                raise FileNotFoundError(f"Could not read image/mask for {row.image}")
            if mask.shape[:2] != image.shape[:2]:
                mask = cv2.resize(mask, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)

            overlay = make_overlay(image, mask)
            stem = f"{object_name}_{row.split}_{row.image.replace('/', '_').replace('\\\\', '_')}"
            out_path = object_dir / f"{stem}.jpg"
            cv2.imwrite(str(out_path), overlay)
            saved.append(out_path)

    print(f"Saved {len(saved)} overlays to {output_dir}")


if __name__ == "__main__":
    main()
