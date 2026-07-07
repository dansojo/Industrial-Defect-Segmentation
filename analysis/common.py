"""Shared helpers for local VisA analysis scripts."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_profiles() -> dict[str, Any]:
    local_path = REPO_ROOT / "configs" / "paths.local.yaml"
    example_path = REPO_ROOT / "configs" / "paths.example.yaml"
    config_path = local_path if local_path.exists() else example_path
    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config["profiles"]


def resolve_profile(profile: str) -> dict[str, Path]:
    profiles = load_profiles()
    if profile not in profiles:
        known = ", ".join(sorted(profiles))
        raise ValueError(f"Unknown profile '{profile}'. Known profiles: {known}")

    raw = profiles[profile]
    data_root = Path(raw["data_root"]).expanduser()
    output_root = Path(raw.get("output_root", "./results")).expanduser()
    if not output_root.is_absolute():
        output_root = REPO_ROOT / output_root

    return {
        "data_root": data_root,
        "output_root": output_root,
    }


def add_common_args(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--profile", default="local_main_laptop")
    parser.add_argument("--split-csv", default="2cls_highshot.csv")
    return parser


def ensure_output_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path
