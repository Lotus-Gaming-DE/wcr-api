from fastapi.testclient import TestClient
import pytest

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


def test_get_unit_with_hyphenated_id():
    response = client.get("/units/ancient-of-war")
    assert response.status_code == 200
    assert response.json()["id"] == "ancient-of-war"


def test_categories_structure():
    response = client.get("/categories")
    assert response.status_code == 200
    categories = response.json()
    assert isinstance(categories, dict)
    assert {"factions", "types", "traits", "speeds"} <= set(categories.keys())


def test_invalid_unit_id_validation():
    response = client.get("/units/invalid!")
    assert response.status_code == 422


def test_units_pagination():
    loader = get_data_loader()
    response = client.get("/units", params={"offset": 1, "limit": 2})
    assert response.status_code == 200
    assert response.json() == loader.units[1:3]


@pytest.mark.parametrize(
    "params",
    [
        {"limit": 0},
        {"limit": 2000},
        {"offset": -1},
    ],
)
def test_units_invalid_pagination_params(params):
    response = client.get("/units", params=params)
    assert response.status_code == 422


def test_dataloader_error_returns_500(monkeypatch):
    from app import api as api_module
    from app.loaders import DataLoadError

    def fail_loader():
        raise DataLoadError("boom")

    monkeypatch.setattr(api_module, "get_data_loader", fail_loader)
    resp = client.get("/units")
    assert resp.status_code == 500
    assert resp.json() == {"detail": "Internal server error"}


def test_logging_middleware_called(caplog):
    with TestClient(app) as c:
        c.get("/units")  # ensure startup has run
        caplog.set_level("INFO")
        c.get("/units")
    import json

    events = []
    for r in caplog.records:
        try:
            data = json.loads(r.getMessage())
            events.append(data.get("event"))
        except json.JSONDecodeError:
            continue
    assert "response" in events
