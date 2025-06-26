"""Utility for loading unit data from JSON files."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


class DataLoadError(Exception):
    """Raised when data files fail to load.

    The API converts this exception into a ``500`` JSON error response so that
    stack traces are not exposed to clients.  The original exception is chained
    to preserve debugging information in the logs.
    """


class DataLoader:
    """Load and cache unit data from JSON files.

    Parameters
    ----------
    data_dir:
        Directory containing ``units.json`` and ``categories.json``.

    The loader builds an index so that :meth:`get_unit_by_id` operates in
    constant time.
    """

    def __init__(self, data_dir: Path) -> None:
        """Create a loader for the given directory.

        Parameters
        ----------
        data_dir:
            Path to the directory containing the data files.
        """

        self.data_dir = data_dir
        self.units: List[Dict[str, Any]] = []
        self.units_by_id: Dict[str, Dict[str, Any]] = {}
        self.categories: Dict[str, Any] = {}

    def load(self) -> None:
        """Load units and categories from JSON files.

        Raises
        ------
        DataLoadError
            If the files cannot be read or parsed. Malformed JSON also
            results in this exception.
        """
        units_file = self.data_dir / "units.json"
        categories_file = self.data_dir / "categories.json"
        try:
            with units_file.open("r", encoding="utf-8") as f:
                self.units = json.load(f)
            with categories_file.open("r", encoding="utf-8") as f:
                self.categories = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            # file read errors or invalid JSON
            raise DataLoadError(str(exc)) from exc

        # build an index so ``get_unit_by_id`` performs constant-time lookups
        self.units_by_id = {unit["id"]: unit for unit in self.units}

    def get_unit_by_id(self, unit_id: str) -> Optional[Dict[str, Any]]:
        """Return a unit dictionary for ``unit_id``.

        Parameters
        ----------
        unit_id:
            Identifier of the unit to fetch.

        Returns
        -------
        dict | None
            Unit data if found, else ``None``.
        """

        return self.units_by_id.get(unit_id)


data_loader: DataLoader | None = None


def get_data_loader() -> DataLoader:
    """Return a cached :class:`DataLoader` instance.

    Returns
    -------
    DataLoader
        Shared loader containing unit and category data.
    """
    global data_loader
    if data_loader is None:
        # resolve the project's root directory and locate the bundled data
        # files. ``parents[2]`` yields the repository root when called from
        # inside ``src/wcr_api``.
        data_dir = Path(__file__).resolve().parents[2] / "data"
        data_loader = DataLoader(data_dir)
        data_loader.load()
    return data_loader
