import json
from pathlib import Path
from typing import Any, Dict, List


class DataLoader:
    """Loads data from JSON files and keeps them in memory."""

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir
        self.units: List[Dict[str, Any]] = []
        self.categories: Dict[str, Any] = {}

    def load(self) -> None:
        """Load units and categories from JSON files."""
        units_file = self.data_dir / "units.json"
        categories_file = self.data_dir / "categories.json"
        with units_file.open("r", encoding="utf-8") as f:
            self.units = json.load(f)
        with categories_file.open("r", encoding="utf-8") as f:
            self.categories = json.load(f)


data_loader: DataLoader | None = None


def get_data_loader() -> DataLoader:
    """Return a singleton DataLoader instance."""
    global data_loader
    if data_loader is None:
        data_loader = DataLoader(Path(__file__).resolve().parent.parent / "data")
        data_loader.load()
    return data_loader
