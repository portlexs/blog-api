import uuid

from fastapi import status
from fastapi.testclient import TestClient


class TestRegisterUser:

    def test_successful_register(self, client: TestClient) -> None:
        user_data = {"email": "test_user@example.com", "password": "password123"}
        create_response = client.post("/api/users/", json=user_data)
        response_data = create_response.json()

        assert create_response.status_code == status.HTTP_200_OK
        assert "id" in response_data
        assert "email" in response_data
        assert response_data["email"] == user_data["email"]
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
        # create user and get his id
        user_data = {"email": "test_user@example.com", "password": "password123"}
        create_response = client.post("/api/users/", json=user_data)
        user_id = create_response.json()["id"]

        # get user by id
        get_response = client.get(f"/api/users/{user_id}")

        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json()["email"] == user_data["email"]
        assert "password" not in get_response.json()

    def test_user_not_found(self, client: TestClient) -> None:
        get_response = client.get(f"/api/users/{uuid.uuid4()}")

        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_invalid_uuid(self, client: TestClient) -> None:
        get_response = client.get("/api/users/1234")

        assert get_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestUpdateUser:

    def test_successful_update_user_email(self, client: TestClient) -> None:
        # create user and get his id
        user_data = {"email": "test_user@example.com", "password": "password123"}
        create_response = client.post("/api/users/", json=user_data)
        user_id = create_response.json()["id"]

        # update user email
        user_data_to_update = {"email": "new_test_user@example.com"}
        update_response = client.put(f"/api/users/{user_id}", json=user_data_to_update)

        assert update_response.status_code == status.HTTP_200_OK

        # login user with new email
        new_user_data = {
            "email": "new_test_user@example.com",
            "password": "password123",
        }
        login_response = client.post("/api/users/login", json=new_user_data)

        assert login_response.status_code == status.HTTP_200_OK

    def test_successful_update_user_password(self, client: TestClient) -> None:
        # create user and get his id
        user_data = {"email": "test_user@example.com", "password": "password123"}
        create_user_response = client.post("/api/users/", json=user_data)
        user_id = create_user_response.json()["id"]

        # update user password
        user_data_to_update = {"password": "new_password123"}
        update_response = client.put(f"/api/users/{user_id}", json=user_data_to_update)

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

    def test_successful_update_user_email_and_password(
        self, client: TestClient
    ) -> None:
        # create user and get his id
        user_data = {"email": "test_user@example.com", "password": "password123"}
        create_response = client.post("/api/users/", json=user_data)
        user_id = create_response.json()["id"]

        # update user email and password
        user_data_to_update = {
            "email": "new_test_user@example.com",
            "password": "new_password123",
        }
        update_response = client.put(f"/api/users/{user_id}", json=user_data_to_update)

        assert update_response.status_code == status.HTTP_200_OK
        assert "password" not in update_response.json()

        # login user with new email and password
        login_response = client.post("/api/users/login", json=user_data_to_update)

        assert login_response.status_code == status.HTTP_200_OK

    def test_updating_user_not_found(self, client: TestClient) -> None:
        user_data = {"email": "test_user@example.com", "password": "password123"}

        update_response = client.put(f"/api/users/{uuid.uuid4()}", json=user_data)

        assert update_response.status_code == status.HTTP_404_NOT_FOUND

    def test_updating_email_already_exists(self, client: TestClient) -> None:
        # create user and get his id
        user_data = {"email": "test_user@example.com", "password": "password123"}
        create_response = client.post("/api/users/", json=user_data)
        user_id = create_response.json()["id"]

        # try to update user email
        user_data_to_update = {"email": "test_user@example.com"}
        update_response = client.put(f"/api/users/{user_id}", json=user_data_to_update)

        assert update_response.status_code == status.HTTP_400_BAD_REQUEST
