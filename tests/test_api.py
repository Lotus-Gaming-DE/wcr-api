from fastapi.testclient import TestClient
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from main import app
from app.loaders import get_data_loader

client = TestClient(app)


def test_units_list_contains_known_id():
    loader = get_data_loader()
    known_id = loader.units[0]["id"]
    response = client.get("/units")
    assert response.status_code == 200
    units = response.json()
    assert isinstance(units, list)
    assert any(u["id"] == known_id for u in units)


def test_get_unit_by_id_or_404():
    loader = get_data_loader()
    unit_id = loader.units[0]["id"]

    resp_ok = client.get(f"/units/{unit_id}")
    assert resp_ok.status_code == 200
    assert resp_ok.json()["id"] == unit_id

    resp_404 = client.get("/units/nonexistent")
    assert resp_404.status_code == 404


def test_categories_structure():
    response = client.get("/categories")
    assert response.status_code == 200
    categories = response.json()
    assert isinstance(categories, dict)
    assert {"factions", "types", "traits", "speeds"} <= set(categories.keys())
