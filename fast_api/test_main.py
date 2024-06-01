import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from typing import AsyncGenerator

from main import app 

@pytest_asyncio.fixture(scope="module")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_save_coins(async_client: AsyncClient):
    response = await async_client.get("/save/1/100")
    assert response.status_code == 200
    assert response.json() == {"message": "Coins saved successfully", "user_id": 1, "coin": 100}

@pytest.mark.asyncio
async def test_get_coins(async_client: AsyncClient): 
    response = await async_client.get("/get/1")
    assert response.status_code == 200
    assert response.json() == {"user_id": 1, "coin": 100}

@pytest.mark.asyncio
async def test_get_nonexistent_user(async_client: AsyncClient):
    response = await async_client.get("/get/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
