from fastapi.testclient import TestClient

from app.loaders import get_data_loader
from main import app


def test_get_unit(monkeypatch):
    client = TestClient(app)

    loader = get_data_loader()
    unit_id = loader.units[0]["id"]
    response = client.get(f"/units/{unit_id}")
    assert response.status_code == 200
    assert response.json()["id"] == unit_id


def test_unit_not_found():
    client = TestClient(app)
    response = client.get("/units/nonexistent")
    assert response.status_code == 404
