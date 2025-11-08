import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_my_model_random(async_client: AsyncClient):
    response = await async_client.get("/")
    assert response.status_code == 200
