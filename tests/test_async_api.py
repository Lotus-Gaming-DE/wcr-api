import pytest
from httpx import AsyncClient, ASGITransport

from main import app


@pytest.mark.asyncio
async def test_list_units_async():
    # use an in-memory transport so no network sockets are opened during tests
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/units")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
