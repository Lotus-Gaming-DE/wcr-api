import json
from pathlib import Path
from typing import Any

import pytest

import scripts.fetch_data as fetch_data


class FakeResponse:
    def __init__(self, data: Any) -> None:
        self._data = data

    def json(self) -> Any:
        return self._data

    def raise_for_status(self) -> None:
        pass


def test_fetch_data(monkeypatch, tmp_path: Path) -> None:
    def fake_get(url: str) -> FakeResponse:
        if url.endswith("/units"):
            return FakeResponse([{"id": "foo"}])
        if url.endswith("/categories"):
            return FakeResponse({"factions": ["bar"]})
        raise ValueError(url)

    monkeypatch.setattr(fetch_data.requests, "get", fake_get)
    monkeypatch.chdir(tmp_path)
    fetch_data.main(["--base-url", "https://example.com", "--output-dir", "."])

    assert json.loads(Path("units.json").read_text()) == [{"id": "foo"}]
    assert json.loads(Path("categories.json").read_text()) == {"factions": ["bar"]}


