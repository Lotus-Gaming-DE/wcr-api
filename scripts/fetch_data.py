"""Download unit and category data from the deployed API."""

from __future__ import annotations

import argparse
import pathlib
import requests


DEFAULT_BASE_URL = "https://wcr-api.up.railway.app"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-u",
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="Base URL of the API",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=pathlib.Path,
        default=pathlib.Path("data"),
        help="Directory to write JSON files",
    )
    return parser.parse_args()


def download_file(url: str, dest: pathlib.Path) -> None:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    dest.write_text(resp.text, encoding="utf-8")


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    download_file(f"{args.base_url}/units", args.output_dir / "units.json")
    download_file(
        f"{args.base_url}/categories",
        args.output_dir / "categories.json",
    )


if __name__ == "__main__":
    main()
