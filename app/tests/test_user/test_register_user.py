from http import HTTPStatus

import pytest

from app.tests.clients.user_client import UserClient


@pytest.mark.asyncio
class TestRegisterUser:
    async def test_successful_register_with_full_data(self, user_client: UserClient):
        register_response = await user_client.register_user(
            {
                "username": "test",
                "email": "email@example.com",
                "password": "password",
                "biography": "test",
                "avatar_url": "https://example.com/avatar.jpg",
            }
        )

        assert register_response.status_code == HTTPStatus.CREATED
        assert "access_token" in register_response.json()
        assert "refresh_token" in register_response.json()

    async def test_successful_register_with_required_data(
        self, user_client: UserClient
    ):
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )

        assert register_response.status_code == HTTPStatus.CREATED
        assert "access_token" in register_response.json()
        assert "refresh_token" in register_response.json()

    async def test_register_user_with_existing_email(self, user_client: UserClient):
        register_response = await user_client.register_user(
            {"username": "test1", "email": "email@example.com", "password": "password1"}
        )

        assert register_response.status_code == HTTPStatus.CREATED

        register_response = await user_client.register_user(
            {"username": "test2", "email": "email@example.com", "password": "password2"}
        )

        assert register_response.status_code == HTTPStatus.BAD_REQUEST

    async def test_register_user_with_existing_username(self, user_client: UserClient):
        register_response = await user_client.register_user(
            {"username": "test", "email": "email1@example.com", "password": "password1"}
        )

        assert register_response.status_code == HTTPStatus.CREATED

        register_response = await user_client.register_user(
            {"username": "test", "email": "email2@example.com", "password": "password2"}
        )

        assert register_response.status_code == HTTPStatus.BAD_REQUEST

    async def test_register_user_with_invalid_email(self, user_client: UserClient):
        register_response = await user_client.register_user(
            {"username": "test", "email": "invalid_email", "password": "password"}
        )

        assert register_response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_register_user_with_invalid_avatar_url(self, user_client: UserClient):
        register_response = await user_client.register_user(
            {
                "username": "test",
                "email": "email@example.com",
                "password": "password",
                "avatar_url": "invalid_url",
            }
        )

        assert register_response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
