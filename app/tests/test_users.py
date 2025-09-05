import uuid

from fastapi import status
from fastapi.testclient import TestClient


class TestRegisterUser:

    def test_successful_register(self, client: TestClient) -> None:
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


class TestLoginUser:

    def test_successful_login(self, client: TestClient) -> None:
        user_data = {"email": "test_user@example.com", "password": "password123"}

        client.post("/api/users/", json=user_data)

        response = client.post("/api/users/login", json=user_data)

        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        # TODO: check if token is valid

    def test_incorrect_email(self, client: TestClient) -> None:
        user_data = {"email": "test_user@example.com", "password": "password123"}

        response = client.post("/api/users/login", json=user_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_incorrect_password(self, client: TestClient) -> None:
        user_data = {"email": "test_user@example.com", "password": "password123"}

        client.post("/api/users/", json=user_data)

        user_data["password"] = "wrong_password"

        response = client.post("/api/users/login", json=user_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_invalid_email(self, client: TestClient) -> None:
        user_data = {"email": "2453656", "password": "password123"}

        response = client.post("/api/users/login", json=user_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_empty_password(self, client: TestClient) -> None:
        user_data = {"email": "test_user@example.com", "password": ""}

        response = client.post("/api/users/login", json=user_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetUser:

    def test_successful_create_and_get_user(self, client: TestClient) -> None:
        user_data = {"email": "test_user@example.com", "password": "password123"}

        response = client.post("/api/users/", json=user_data)

        response = client.get(f"/api/users/{response.json()['id']}")

        assert response.status_code == status.HTTP_200_OK
        assert "id" in response.json()
        assert "email" in response.json()
        assert response.json()["email"] == user_data["email"]
        assert "password" not in response.json()

    def test_user_not_found(self, client: TestClient) -> None:
        response = client.get(f"/api/users/{uuid.uuid4()}")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_invalid_uuid(self, client: TestClient) -> None:
        response = client.get("/api/users/invalid_uuid")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
