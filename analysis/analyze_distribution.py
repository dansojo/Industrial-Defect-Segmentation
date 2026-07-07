"""Analyze normal/anomaly distribution by VisA category."""

from __future__ import annotations

import pandas as pd

from common import add_common_args, ensure_output_dir, resolve_profile


def main() -> None:
    parser = add_common_args("Analyze normal/anomaly distribution by category.")
    args = parser.parse_args()

    profile = resolve_profile(args.profile)
    data_root = profile["data_root"]
    output_root = ensure_output_dir(profile["output_root"])

    df = pd.read_csv(data_root / "split_csv" / args.split_csv)
    distribution = (
        df.groupby(["object", "split", "label"])
        .size()
        .rename("count")
        .reset_index()
        .sort_values(["object", "split", "label"])
    )
    pivot = (
        distribution.pivot_table(
            index=["object", "split"],
            columns="label",
            values="count",
            fill_value=0,
        )
        .reset_index()
        .rename_axis(None, axis=1)
    )

    output_path = output_root / "dataset_distribution.csv"
    pivot.to_csv(output_path, index=False)

    print(pivot.to_string(index=False))
    print(f"\nSaved: {output_path}")


if __name__ == "__main__":
    main()
