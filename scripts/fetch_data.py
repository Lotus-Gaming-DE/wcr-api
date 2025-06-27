"""Fetch unit and category data from the hosted API."""

import argparse
import json
import os
from pathlib import Path
from typing import Sequence

import requests


def main(argv: Sequence[str] | None = None) -> None:
    """Download JSON data from the production API.

    Parameters
    ----------
    argv:
        Optional sequence of arguments. If ``None`` the arguments are taken
        from ``sys.argv``.
    """
    parser = argparse.ArgumentParser(description="Download data from the WCR API")
    parser.add_argument(
        "--base-url",
        default="https://wcr-api.up.railway.app",
        help="Base URL of the API",
    )
    parser.add_argument(
        "--output-dir",
        default="data",
        help="Directory to store downloaded JSON files",
    )
    args = parser.parse_args(argv)

    os.makedirs(args.output_dir, exist_ok=True)
    for name in ["units", "categories"]:
        resp = requests.get(f"{args.base_url.rstrip('/')}/{name}")
        resp.raise_for_status()
        out_file = Path(args.output_dir) / f"{name}.json"
        with out_file.open("w", encoding="utf-8") as f:
            json.dump(resp.json(), f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()

