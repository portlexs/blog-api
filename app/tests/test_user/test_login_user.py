from http import HTTPStatus

import pytest

from app.tests.clients.user_client import UserClient


@pytest.mark.asyncio
class TestLoginUser:
    async def test_successful_login_with_email(self, user_client: UserClient) -> None:
        await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )

        login_response = await user_client.login_user(
            {"login": "email@example.com", "password": "password"}
        )

        assert login_response.status_code == HTTPStatus.OK
        assert "access_token" in login_response.json()
        assert "refresh_token" in login_response.cookies

    async def test_successful_login_with_username(
        self, user_client: UserClient
    ) -> None:
        await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )

        login_response = await user_client.login_user(
            {"login": "test", "password": "password"}
        )

        assert login_response.status_code == HTTPStatus.OK

    async def test_login_with_incorrect_email(self, user_client: UserClient) -> None:
        await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )

        login_response = await user_client.login_user(
            {"login": "wrong_email", "password": "password"}
        )

        assert login_response.status_code == HTTPStatus.UNAUTHORIZED

    async def test_login_with_incorrect_username(self, user_client: UserClient) -> None:
        await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )

        login_response = await user_client.login_user(
            {"login": "wrong_username", "password": "password"}
        )

        assert login_response.status_code == HTTPStatus.UNAUTHORIZED

    async def test_login_with_incorrect_password(self, user_client: UserClient) -> None:
        await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )

        login_response = await user_client.login_user(
            {"login": "email@example.com", "password": "wrong_password"}
        )

        assert login_response.status_code == HTTPStatus.UNAUTHORIZED

    async def test_login_with_not_active_user(self, user_client: UserClient) -> None:
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        access_token = register_response.json()["access_token"]

        await user_client.delete_user(
            headers={"Authorization": f"Bearer {access_token}"}
        )

        login_response = await user_client.login_user(
            {"login": "email@example.com", "password": "password"}
        )

        assert login_response.status_code == HTTPStatus.UNAUTHORIZED
