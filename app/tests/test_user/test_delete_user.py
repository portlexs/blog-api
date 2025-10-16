from http import HTTPStatus

import pytest

from app.tests.clients.user_client import UserClient


@pytest.mark.asyncio
class TestDeleteUser:
    async def test_successful_delete_user(self, user_client: UserClient) -> None:
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        access_token = register_response.json()["access_token"]

        delete_user_response = await user_client.delete_user(
            headers={"Authorization": f"Bearer {access_token}"}
        )

        assert delete_user_response.status_code == HTTPStatus.NO_CONTENT

    async def test_unauthorized_delete_user(self, user_client: UserClient) -> None:
        delete_user_response = await user_client.delete_user(
            headers={"Authorization": "Bearer token"}
        )

        assert delete_user_response.status_code == HTTPStatus.UNAUTHORIZED
