"""Download unit and category JSON files for local development."""

import argparse
import json
from pathlib import Path
from typing import Final

import requests

DEFAULT_BASE_URL: Final[str] = "https://wcr-api.up.railway.app"


def download_file(url: str, dest: Path) -> None:
    """Fetch ``url`` and write the response JSON to ``dest``."""
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    dest.write_text(json.dumps(resp.json(), indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="Base URL of the API",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data"),
        help="Directory to write downloaded files",
    )
    return parser.parse_args()


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
