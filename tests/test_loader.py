import json
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.loaders import DataLoader, DataLoadError


def test_load_success(tmp_path):
    # copy data files to temporary directory
    data_dir = tmp_path
    units_data = [{"id": "a", "value": 1}]
    categories_data = {"cats": []}
    (data_dir / "units.json").write_text(json.dumps(units_data))
    (data_dir / "categories.json").write_text(json.dumps(categories_data))

    loader = DataLoader(data_dir)
    loader.load()

    assert loader.units == units_data
    assert loader.categories == categories_data
    assert loader.get_unit_by_id("a") == units_data[0]


def test_load_missing_file(tmp_path):
    loader = DataLoader(tmp_path)
    with pytest.raises(DataLoadError):
        loader.load()
