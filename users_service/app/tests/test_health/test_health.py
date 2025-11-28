from http import HTTPStatus

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health(client: AsyncClient) -> None:
    health_response = await client.get("/api/health")

    assert health_response.status_code == HTTPStatus.OK
