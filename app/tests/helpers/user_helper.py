from typing import Any, Dict

from fastapi.testclient import TestClient
from httpx import Response


class DefaultUser:
    def __init__(self, client: TestClient) -> None:
        self.client = client
        self.username = "test_user"
        self.email = "test_user@example.com"
        self.password = "password123"
        self.bio = "Test user bio"
        self.image_url = "https://example.com/test_user.jpg"

    def register(self) -> Response:
        json = {
            "email": self.email,
            "password": self.password,
            "username": self.username,
            "bio": self.bio,
            "image_url": self.image_url,
        }
        return self.client.post("/api/users/", json=json)

    def login(self) -> Response:
        json = {"email": self.email, "password": self.password}
        return self.client.post("/api/users/login", json=json)

    def register_and_login(self) -> str:
        self.register()
        login_response = self.login()
        return login_response.json()["access_token"]


class UserHelper:
    def __init__(self, client: TestClient) -> None:
        self.client = client
        self.default_user = DefaultUser(client)

    def get_user(self, headers: Dict[str, str]) -> Response:
        return self.client.get("/api/users/me", headers=headers)

    def register_user(
        self,
        email: str,
        password: str,
        username: str | None = None,
        bio: str | None = None,
        image_url: str | None = None,
    ) -> Response:
        user_data = {
            "email": email,
            "password": password,
            "username": username,
            "bio": bio,
            "image_url": image_url,
        }
        return self.client.post("/api/users/", json=user_data)

    def login_user(self, email: str, password: str) -> Response:
        user_data = {"email": email, "password": password}
        return self.client.post("/api/users/login", json=user_data)

    def update_user(
        self, headers: Dict[str, str], user_data: Dict[str, Any]
    ) -> Response:
        return self.client.put("/api/users/me", headers=headers, json=user_data)

    def refresh_user_token(self, refresh_token: str) -> Response:
        return self.client.post(
            "/api/users/refresh", params={"refresh_token": refresh_token}
        )
