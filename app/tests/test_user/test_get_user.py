from http import HTTPStatus

import pytest

from app.tests.clients.user_client import UserClient


@pytest.mark.asyncio
class TestGetUser:
    async def test_successful_get_user(self, user_client: UserClient) -> None:
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        access_token = register_response.json()["access_token"]

        get_user_response = await user_client.get_current_user(
            headers={"Authorization": f"Bearer {access_token}"}
        )

        assert get_user_response.status_code == HTTPStatus.OK

    async def test_unauthorized_get_user(self, user_client: UserClient) -> None:
        get_user_response = await user_client.get_current_user(
            headers={"Authorization": "Bearer token"}
        )

        assert get_user_response.status_code == HTTPStatus.UNAUTHORIZED
