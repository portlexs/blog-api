from fastapi import status
from fastapi.testclient import TestClient


class TestRegisterUser:

    def test_user_registered_in_db(self, client: TestClient) -> None:
        user_data = {"email": "test_user@example.com", "password": "password123"}

        response = client.post("/api/users/", json=user_data)
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert "id" in response_data
        assert "email" in response_data
        assert response_data["email"] == user_data["email"]
        assert "password" not in response_data

    def test_email_exists(self, client: TestClient) -> None:
        user_data = {"email": "test_user@example.com", "password": "password123"}

        client.post("/api/users/", json=user_data)

        response = client.post("/api/users/", json=user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Email already registered"}

    def test_invalid_email(self, client: TestClient) -> None:
        user_data = {"email": "invalid_email", "password": "password123"}

        response = client.post("/api/users/", json=user_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_empty_email(self, client: TestClient) -> None:
        user_data = {"email": "", "password": "password123"}

        response = client.post("/api/users/", json=user_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_empty_password(self, client: TestClient) -> None:
        user_data = {"email": "test_user@example.com", "password": ""}

        response = client.post("/api/users/", json=user_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
