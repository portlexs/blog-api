from http import HTTPStatus

import pytest

from app.tests.clients.user_client import UserClient


@pytest.mark.asyncio
class TestTokens:
    async def test_successful_refresh_token(self, user_client: UserClient) -> None:
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        refresh_token = register_response.cookies["refresh_token"]

        refresh_response = await user_client.refresh_token(refresh_token)

        assert refresh_response.status_code == HTTPStatus.OK
        assert "access_token" in refresh_response.json()
        assert "refresh_token" in refresh_response.cookies

    async def test_refresh_token_is_revoked(self, user_client: UserClient) -> None:
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        refresh_token = register_response.cookies["refresh_token"]

        await user_client.refresh_token(refresh_token)

        refresh_response = await user_client.refresh_token(refresh_token=refresh_token)

        assert refresh_response.status_code == HTTPStatus.UNAUTHORIZED

    async def test_refresh_token_with_access_token(
        self, user_client: UserClient
    ) -> None:
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        access_token = register_response.json()["access_token"]

        refresh_response = await user_client.refresh_token(refresh_token=access_token)

        assert refresh_response.status_code == HTTPStatus.UNAUTHORIZED

    async def test_refresh_token_with_not_active_user(
        self, user_client: UserClient
    ) -> None:
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        access_token = register_response.json()["access_token"]
        refresh_token = register_response.cookies["refresh_token"]

        await user_client.delete_user(
            headers={"Authorization": f"Bearer {access_token}"}
        )

        refresh_response = await user_client.refresh_token(refresh_token)

        assert refresh_response.status_code == HTTPStatus.UNAUTHORIZED

    async def test_refresh_token_with_empty_invalid_token(
        self, user_client: UserClient
    ) -> None:
        refresh_response = await user_client.refresh_token(
            refresh_token="invalid_token"
        )

        assert refresh_response.status_code == HTTPStatus.UNAUTHORIZED

    async def test_refresh_token_without_token(self, user_client: UserClient) -> None:
        refresh_response = await user_client.refresh_token(refresh_token=None)

        assert refresh_response.status_code == HTTPStatus.UNAUTHORIZED
