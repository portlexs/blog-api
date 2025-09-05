from fastapi import status
from fastapi.testclient import TestClient


class TestUserRegister:

    def test_register_user_success(self, client: TestClient) -> None:
        user_data = {"email": "test_user@example.com", "password": "password123"}

        response = client.post("/api/users/", json=user_data)

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()

        assert "id" in response_data
        assert "email" in response_data
        assert response_data["email"] == user_data["email"]

        assert "password" not in response_data

    def test_register_user_email_exists(self, client: TestClient) -> None:
        user_data = {"email": "test_user@example.com", "password": "password123"}

        client.post("/api/users/", json=user_data)

        response = client.post("/api/users/", json=user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Email already registered"}

    def test_register_user_invalid_email(self, client: TestClient) -> None:
        user_data = {"email": "invalid_email", "password": "password123"}

        response = client.post("/api/users/", json=user_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_user_empty_password(self, client: TestClient) -> None:
        user_data = {"email": "test_user@example.com", "password": ""}

        response = client.post("/api/users/", json=user_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
