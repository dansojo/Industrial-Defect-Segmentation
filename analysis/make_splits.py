"""Generate train/validation/test split CSVs for reproducible experiments."""

from __future__ import annotations

import pandas as pd

from common import add_common_args, ensure_output_dir, resolve_profile, REPO_ROOT


def stratified_val_split(df: pd.DataFrame, val_ratio: float, seed: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    train_parts = []
    val_parts = []
    grouped = df.groupby(["object", "label"], sort=False)
    for _, group in grouped:
        shuffled = group.sample(frac=1.0, random_state=seed)
        val_count = max(1, round(len(shuffled) * val_ratio))
        val_parts.append(shuffled.iloc[:val_count])
        train_parts.append(shuffled.iloc[val_count:])

    return pd.concat(train_parts), pd.concat(val_parts)


def main() -> None:
    parser = add_common_args("Create a train/val/test split from an official VisA split CSV.")
    parser.add_argument("--val-ratio", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-name", default="visa_2cls_highshot_train_val_test.csv")
    args = parser.parse_args()

    profile = resolve_profile(args.profile)
    data_root = profile["data_root"]
    df = pd.read_csv(data_root / "split_csv" / args.split_csv)

    train_df = df[df["split"] == "train"].copy()
    test_df = df[df["split"] == "test"].copy()
    train_part, val_part = stratified_val_split(train_df, args.val_ratio, args.seed)
    train_part = train_part.copy()
    val_part = val_part.copy()
    test_df = test_df.copy()
    train_part["split"] = "train"
    val_part["split"] = "val"
    test_df["split"] = "test"

    output = pd.concat([train_part, val_part, test_df], ignore_index=True)
    output = output.sort_values(["split", "object", "label", "image"]).reset_index(drop=True)

    out_dir = ensure_output_dir(REPO_ROOT / "data" / "splits")
    out_path = out_dir / args.output_name
    output.to_csv(out_path, index=False)

    print(output.groupby(["split", "label"]).size().unstack(fill_value=0).to_string())
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
