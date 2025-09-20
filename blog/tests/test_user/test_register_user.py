from fastapi import status

from tests.clients.user_client import UserClient


class TestRegisterUser:
    async def test_successful_register(self, user_client: UserClient) -> None:
        register_response = await user_client.register_user(
            user_data=user_client.default_data
        )
        assert register_response.status_code == status.HTTP_201_CREATED
