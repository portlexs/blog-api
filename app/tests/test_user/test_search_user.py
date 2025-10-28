from http import HTTPStatus

import pytest

from app.tests.clients.user_client import UserClient


@pytest.mark.asyncio
class TestSearchUser:
    async def test_successful_search_user(self, user_client: UserClient) -> None:
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        access_token = register_response.json()["access_token"]

        search_response = await user_client.search_user(
            {"username": "test"}, headers={"Authorization": f"Bearer {access_token}"}
        )

        assert search_response.status_code == HTTPStatus.OK

    async def test_unauthorized_search_user(self, user_client: UserClient) -> None:
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )

        search_response = await user_client.search_user(
            {"username": "test"}, headers=None
        )

        assert search_response.status_code == HTTPStatus.OK

    async def test_search_user_not_found(self, user_client: UserClient) -> None:
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        access_token = register_response.json()["access_token"]

        search_response = await user_client.search_user(
            {"username": "not_found"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert search_response.status_code == HTTPStatus.NOT_FOUND

    async def test_search_user_with_empty_username(
        self, user_client: UserClient
    ) -> None:
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        access_token = register_response.json()["access_token"]

        search_response = await user_client.search_user(
            {"username": ""}, headers={"Authorization": f"Bearer {access_token}"}
        )

        assert search_response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
