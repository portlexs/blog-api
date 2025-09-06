from fastapi import status
from fastapi.testclient import TestClient

from core import jwt


class TestRegisterUser:

    def test_successful_register(self, client: TestClient) -> None:
        user_data = {"email": "test_user@example.com", "password": "password123"}
        create_response = client.post("/api/users/", json=user_data)
        response_data = create_response.json()

        assert create_response.status_code == status.HTTP_200_OK
        assert "email" in response_data and response_data["email"] == user_data["email"]
        assert "password" not in response_data

    def test_email_exists(self, client: TestClient) -> None:
        # create user
        user_data = {"email": "test_user@example.com", "password": "password123"}
        client.post("/api/users/", json=user_data)

        # try to create user with the same email
        response = client.post("/api/users/", json=user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_invalid_email(self, client: TestClient) -> None:
        user_data = {"email": "invalid_email", "password": "password123"}

        create_response = client.post("/api/users/", json=user_data)

        assert create_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_empty_email(self, client: TestClient) -> None:
        # create user with empty email
        user_data = {"email": "", "password": "password123"}
        create_response = client.post("/api/users/", json=user_data)

        assert create_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        # create user with absend email
        user_data = {"password": "password123"}
        create_response = client.post("/api/users/", json=user_data)

        assert create_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_empty_password(self, client: TestClient) -> None:
        user_data = {"email": "test_user@example.com", "password": ""}

        response = client.post("/api/users/", json=user_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestLoginUser:

    def test_successful_login(self, client: TestClient) -> None:
        # create user
        user_data = {"email": "test_user@example.com", "password": "password123"}
        client.post("/api/users/", json=user_data)

        # login user
        login_response = client.post("/api/users/login", json=user_data)

        assert login_response.status_code == status.HTTP_200_OK
        assert "access_token" in login_response.json()
        # TODO: check if token is valid

    def test_incorrect_email(self, client: TestClient) -> None:
        user_data = {"email": "test_user@example.com", "password": "password123"}
        response = client.post("/api/users/login", json=user_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_incorrect_password(self, client: TestClient) -> None:
        # create user
        user_data = {"email": "test_user@example.com", "password": "password123"}
        client.post("/api/users/", json=user_data)

        # login user with incorrect password
        user_data["password"] = "wrong_password"
        login_response = client.post("/api/users/login", json=user_data)

        assert login_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_invalid_email(self, client: TestClient) -> None:
        user_data = {"email": "2453656", "password": "password123"}
        login_response = client.post("/api/users/login", json=user_data)

        assert login_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_empty_password(self, client: TestClient) -> None:
        user_data = {"email": "test_user@example.com", "password": ""}
        login_response = client.post("/api/users/login", json=user_data)

        assert login_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetUser:

    def test_successful_create_and_get_user(self, client: TestClient) -> None:
        # create user
        user_data = {"email": "test_user@example.com", "password": "password123"}
        client.post("/api/users/", json=user_data)

        # login user
        login_response = client.post("/api/users/login", json=user_data)
        access_token = login_response.json()["access_token"]

        # get user
        get_response = client.get(
            f"/api/users/me", headers={"Authorization": f"Bearer {access_token}"}
        )

        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json()["email"] == user_data["email"]
        assert "password" not in get_response.json()

    def test_user_unauthorized(self, client: TestClient) -> None:
        get_response = client.get("/api/users/me")

        assert get_response.status_code == status.HTTP_401_UNAUTHORIZED


class TestUpdateUser:

    def test_successful_update_user_email(self, client: TestClient) -> None:
        # create user
        user_data = {"email": "test_user@example.com", "password": "password123"}
        client.post("/api/users/", json=user_data)

        # login user
        login_response = client.post("/api/users/login", json=user_data)
        access_token = login_response.json()["access_token"]

        # update user email
        user_data_to_update = {"email": "new_test_user@example.com"}
        update_response = client.put(
            f"/api/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
            json=user_data_to_update,
        )

        assert update_response.status_code == status.HTTP_200_OK

        # login user with new email
        new_user_data = {
            "email": "new_test_user@example.com",
            "password": "password123",
        }
        login_response = client.post("/api/users/login", json=new_user_data)

        assert login_response.status_code == status.HTTP_200_OK
        assert "access_token" in login_response.json()

    def test_successful_update_user_password(self, client: TestClient) -> None:
        # create user
        user_data = {"email": "test_user@example.com", "password": "password123"}
        client.post("/api/users/", json=user_data)

        # login user
        login_response = client.post("/api/users/login", json=user_data)
        access_token = login_response.json()["access_token"]

        # update user password
        user_data_to_update = {"password": "new_password123"}
        update_response = client.put(
            f"/api/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
            json=user_data_to_update,
        )

        assert update_response.status_code == status.HTTP_200_OK
        assert "password" not in update_response.json()

        # login user with new password
        new_user_data = {
            "email": "test_user@example.com",
            "password": "new_password123",
        }
        login_response = client.post("/api/users/login", json=new_user_data)

        assert login_response.status_code == status.HTTP_200_OK
        assert "access_token" in login_response.json()

    def test_updating_user_unauthorized(self, client: TestClient) -> None:
        user_data = {"email": "test_user@example.com", "password": "password123"}

        update_response = client.put(f"/api/users/me", json=user_data)

        assert update_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_updating_email_already_exists(self, client: TestClient) -> None:
        # create user
        user_data = {"email": "test_user@example.com", "password": "password123"}
        client.post("/api/users/", json=user_data)

        # login user
        login_response = client.post("/api/users/login", json=user_data)
        access_token = login_response.json()["access_token"]

        # try to update user email
        user_data_to_update = {"email": "test_user@example.com"}
        update_response = client.put(
            f"/api/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
            json=user_data_to_update,
        )

        assert update_response.status_code == status.HTTP_400_BAD_REQUEST


class TestRefreshToken:

    def test_successful_refresh_token(self, client: TestClient) -> None:
        # create user
        user_data = {"email": "test_user@example.com", "password": "password123"}
        client.post("/api/users/", json=user_data)

        # login user
        login_response = client.post("/api/users/login", json=user_data)
        access_token = login_response.json()["access_token"]
        refresh_token = login_response.json()["refresh_token"]

        # refresh token
        refresh_response = client.post(
            "/api/users/refresh", params={"refresh_token": refresh_token}
        )
        new_tokens = refresh_response.json()

        assert refresh_response.status_code == status.HTTP_200_OK
        assert "access_token" in new_tokens and "refresh_token" in new_tokens

        assert new_tokens["access_token"] != access_token
        assert new_tokens["refresh_token"] != refresh_token

        assert jwt.decode_token(new_tokens["access_token"]) is not None
        assert jwt.decode_token(new_tokens["refresh_token"]) is not None

    def test_refresh_with_access_token(self, client: TestClient) -> None:
        # create user
        user_data = {"email": "test_user@example.com", "password": "password123"}
        client.post("/api/users/", json=user_data)

        # login user
        login_response = client.post("/api/users/login", json=user_data)
        access_token = login_response.json()["access_token"]

        # refresh token with access token
        refresh_response = client.post(
            "/api/users/refresh", params={"refresh_token": access_token}
        )

        assert refresh_response.status_code == status.HTTP_401_UNAUTHORIZED
