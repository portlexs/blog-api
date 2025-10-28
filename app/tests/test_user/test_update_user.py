from http import HTTPStatus

import pytest

from app.tests.clients.user_client import UserClient


@pytest.mark.asyncio
class TestUpdateUser:
    async def test_successful_update_user(self, user_client: UserClient) -> None:
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        access_token = register_response.json()["access_token"]

        update_user_response = await user_client.update_user(
            {
                "email": "new_email@example.com",
                "username": "new_test",
                "password": "new_password",
                "biography": "new_biography",
                "avatar_url": "http://example.com/new_avatar.jpg",
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert update_user_response.status_code == HTTPStatus.OK

    async def test_update_user_with_existing_email(
        self, user_client: UserClient
    ) -> None:
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        access_token = register_response.json()["access_token"]

        update_user_response = await user_client.update_user(
            {"email": "email@example.com"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert update_user_response.status_code == HTTPStatus.CONFLICT

    async def test_update_user_with_existing_username(
        self, user_client: UserClient
    ) -> None:
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        access_token = register_response.json()["access_token"]

        update_user_response = await user_client.update_user(
            {"username": "test"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert update_user_response.status_code == HTTPStatus.CONFLICT

    async def test_update_user_with_existig_username_and_email(
        self, user_client: UserClient
    ) -> None:
        register_response = await user_client.register_user(
            {"username": "test1", "email": "email1@example.com", "password": "password"}
        )

        register_response = await user_client.register_user(
            {"username": "test2", "email": "email2@example.com", "password": "password"}
        )
        access_token = register_response.json()["access_token"]

        update_user_response = await user_client.update_user(
            {"username": "test1", "email": "email2@example.com"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert update_user_response.status_code == HTTPStatus.CONFLICT
