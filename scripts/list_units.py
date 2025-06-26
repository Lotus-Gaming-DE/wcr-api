"""List WCR units or display a single unit by ID."""

import argparse
from pathlib import Path
import json

from wcr_api.loaders import DataLoader


def main() -> None:
    """Command-line interface for listing unit information."""
    parser = argparse.ArgumentParser(description="List units from units.json")
    parser.add_argument("unit_id", nargs="?", help="ID of the unit to display")
    args = parser.parse_args()

    data_dir = Path(__file__).resolve().parents[1] / "data"
    loader = DataLoader(data_dir)
    loader.load()

    if args.unit_id:
        unit = loader.get_unit_by_id(args.unit_id)
        if unit is None:
            print(f"Unit {args.unit_id} not found")
            return
        print(json.dumps(unit, indent=2))
    else:
        for unit in loader.units:
            print(unit["id"])


if __name__ == "__main__":
    main()
