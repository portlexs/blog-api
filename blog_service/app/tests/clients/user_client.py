from typing import Dict, Optional

from httpx import AsyncClient, Response


class UserClient:
    def __init__(self, client: AsyncClient) -> None:
        self.client = client
        self.base_url = "/api/users"

    async def get_current_user(self, headers: Optional[Dict]) -> Response:
        return await self.client.get(f"{self.base_url}/me", headers=headers)

    async def register_user(self, user_in: Dict) -> Response:
        return await self.client.post(f"{self.base_url}/register", json=user_in)

    async def login_user(self, user_in: Dict) -> Response:
        return await self.client.post(f"{self.base_url}/login", json=user_in)

    async def update_user(self, user_in: Dict, headers: Optional[Dict]) -> Response:
        return await self.client.put(
            f"{self.base_url}/me/update", json=user_in, headers=headers
        )

    async def delete_user(self, headers: Optional[Dict]) -> Response:
        return await self.client.delete(f"{self.base_url}/me/delete", headers=headers)

    async def search_user(self, user_in: Dict, headers: Optional[Dict]) -> Response:
        return await self.client.get(
            f"{self.base_url}/search", params=user_in, headers=headers
        )

    async def refresh_token(self, refresh_token: str) -> Response:
        self.client.cookies.set("refresh_token", refresh_token)
        return await self.client.post(f"{self.base_url}/me/refresh")
