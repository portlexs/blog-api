from typing import Any, Dict

from fastapi.testclient import TestClient
from httpx import Response


class UserHelper:
    def __init__(self, client: TestClient) -> None:
        self.client = client
        self.default_username = "test_user"
        self.default_email = "test_user@example.com"
        self.default_password = "password123"

    def get_user(self, access_token: str) -> Response:
        headers = {"Authorization": f"Bearer {access_token}"}
        return self.client.get("/api/users/me", headers=headers)

    def create_user(
        self, email: str, password: str, username: str | None = None
    ) -> Response:
        user_data = {
            "email": email,
            "password": password,
            "username": username or self.default_username,
        }
        return self.client.post("/api/users/", json=user_data)

    def create_default_user(self) -> Response:
        return self.create_user(self.default_email, self.default_password)

    def login_user(self, email: str, password: str) -> Response:
        user_data = {"email": email, "password": password}
        return self.client.post("/api/users/login", json=user_data)

    def login_default_user(self) -> Response:
        return self.login_user(self.default_email, self.default_password)

    def update_user(self, access_token: str, user_data: Dict[str, Any]) -> Response:
        headers = {"Authorization": f"Bearer {access_token}"}
        return self.client.put("/api/users/me", headers=headers, json=user_data)

    def refresh_user_token(self, refresh_token: str) -> Response:
        return self.client.post(
            "/api/users/refresh", params={"refresh_token": refresh_token}
        )
