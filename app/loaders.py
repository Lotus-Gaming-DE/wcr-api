import json
from pathlib import Path
from typing import Any, Dict, List, Optional


class DataLoadError(Exception):
    """Raised when data files fail to load."""


class DataLoader:
    """Loads data from JSON files and stores them for quick access.

    Units are indexed by ID to provide constant-time lookups via
    :meth:`get_unit_by_id`.
    """

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir
        self.units: List[Dict[str, Any]] = []
        self.units_by_id: Dict[str, Dict[str, Any]] = {}
        self.categories: Dict[str, Any] = {}

    def load(self) -> None:
        """Load units and categories from JSON files."""
        units_file = self.data_dir / "units.json"
        categories_file = self.data_dir / "categories.json"
        try:
            with units_file.open("r", encoding="utf-8") as f:
                self.units = json.load(f)
            with categories_file.open("r", encoding="utf-8") as f:
                self.categories = json.load(f)
        except OSError as exc:  # file read errors
            raise DataLoadError(str(exc)) from exc

        self.units_by_id = {unit["id"]: unit for unit in self.units}

    def get_unit_by_id(self, unit_id: str) -> Optional[Dict[str, Any]]:
        """Return a unit by its ID using an efficient dictionary lookup."""
        return self.units_by_id.get(unit_id)


data_loader: DataLoader | None = None


def get_data_loader() -> DataLoader:
    """Return a singleton DataLoader instance."""
    global data_loader
    if data_loader is None:
        data_loader = DataLoader(Path(__file__).resolve().parent.parent / "data")
        data_loader.load()
    return data_loader
