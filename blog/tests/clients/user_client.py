from httpx import AsyncClient, Response


class UserClient:
    def __init__(self, client: AsyncClient) -> None:
        self.client = client
        self.default_data = {
            "username": "testuser",
            "email": "test@gmail.com",
            "password": "testpassword",
            "biography": "test biography",
            "avatar_url": "https://example.com/avatar.jpg",
        }

    async def register_user(self, user_data: dict) -> Response:
        return await self.client.post("/api/users/register", json=user_data)
