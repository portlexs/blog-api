from fastapi import status

from core import jwt
from helpers.user_helper import UserHelper


class TestRegisterUser:

    def test_successful_register(self, user_helper: UserHelper) -> None:
        create_response = user_helper.create_default_user()
        create_response_data = create_response.json()

        assert create_response.status_code == status.HTTP_200_OK
        assert (
            "email" in create_response_data
            and create_response_data["email"] == user_helper.default_email
        )
        assert "password" not in create_response_data

    def test_email_exists(self, user_helper: UserHelper) -> None:
        user_helper.create_default_user()
        create_response = user_helper.create_default_user()

        assert create_response.status_code == status.HTTP_400_BAD_REQUEST

    def test_invalid_email(self, user_helper: UserHelper) -> None:
        create_response = user_helper.create_user("invalid_email", "password123")

        assert create_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_empty_email(self, user_helper: UserHelper) -> None:
        create_response1 = user_helper.create_user("", "password123")
        create_response2 = user_helper.create_user(None, "password123")

        assert create_response1.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert create_response2.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_empty_password(self, user_helper: UserHelper) -> None:
        create_response = user_helper.create_user("test_user@example.com", "")

        assert create_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestLoginUser:

    def test_successful_login(self, user_helper: UserHelper) -> None:
        user_helper.create_default_user()
        login_response = user_helper.login_default_user()

        assert login_response.status_code == status.HTTP_200_OK

        assert "access_token" in login_response.json()
        access_token = login_response.json()["access_token"]
        assert jwt.decode_token(access_token) is not None

        assert "refresh_token" in login_response.json()
        refresh_token = login_response.json()["refresh_token"]
        assert jwt.decode_token(refresh_token) is not None

    def test_incorrect_email(self, user_helper: UserHelper) -> None:
        login_response = user_helper.login_user("test_user@example.com", "password123")

        assert login_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_incorrect_password(self, user_helper: UserHelper) -> None:
        user_helper.create_default_user()
        login_response = user_helper.login_user(
            user_helper.default_email, "wrong_password"
        )

        assert login_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_invalid_email(self, user_helper: UserHelper) -> None:
        login_response = user_helper.login_user("invalid_email", "password123")

        assert login_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_empty_password(self, user_helper: UserHelper) -> None:
        login_response = user_helper.login_user("test_user@example.com", "")

        assert login_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetUser:

    def test_successful_create_and_get_user(self, user_helper: UserHelper) -> None:
        user_helper.create_default_user()
        login_response = user_helper.login_default_user()
        access_token = login_response.json()["access_token"]

        get_response = user_helper.get_user(access_token)

        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json()["email"] == user_helper.default_email
        assert "password" not in get_response.json()

    def test_user_unauthorized(self, user_helper: UserHelper) -> None:
        get_response = user_helper.get_user(access_token=None)

        assert get_response.status_code == status.HTTP_401_UNAUTHORIZED


class TestUpdateUser:

    def test_successful_update_user_email(self, user_helper: UserHelper) -> None:
        user_helper.create_default_user()
        login_response = user_helper.login_default_user()
        access_token = login_response.json()["access_token"]

        # update user email
        user_data_to_update = {"email": "new_test_user@example.com"}
        update_response = user_helper.update_user(access_token, user_data_to_update)

        assert update_response.status_code == status.HTTP_200_OK

        login_response = user_helper.login_user(
            "new_test_user@example.com", user_helper.default_password
        )

        assert login_response.status_code == status.HTTP_200_OK

    def test_successful_update_user_password(self, user_helper: UserHelper) -> None:
        user_helper.create_default_user()
        login_response = user_helper.login_default_user()
        access_token = login_response.json()["access_token"]

        # update user password
        user_data_to_update = {"password": "new_password123"}
        update_response = user_helper.update_user(access_token, user_data_to_update)

        assert update_response.status_code == status.HTTP_200_OK

        # login user with new password
        login_response = user_helper.login_user(
            user_helper.default_email, "new_password123"
        )

        assert login_response.status_code == status.HTTP_200_OK

    def test_updating_user_unauthorized(self, user_helper: UserHelper) -> None:
        user_data = {"email": "test_user@example.com", "password": "password123"}

        update_response = user_helper.update_user(
            access_token=None, user_data=user_data
        )

        assert update_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_updating_email_already_exists(self, user_helper: UserHelper) -> None:
        user_helper.create_default_user()
        login_response = user_helper.login_default_user()
        access_token = login_response.json()["access_token"]

        # try to update user email
        user_data_to_update = {"email": "test_user@example.com"}
        update_response = user_helper.update_user(access_token, user_data_to_update)

        assert update_response.status_code == status.HTTP_400_BAD_REQUEST


class TestRefreshToken:

    def test_successful_refresh_token(self, user_helper: UserHelper) -> None:
        user_helper.create_default_user()

        login_response = user_helper.login_default_user()
        access_token = login_response.json()["access_token"]
        refresh_token = login_response.json()["refresh_token"]

        # refresh token
        refresh_response = user_helper.refresh_user_token(refresh_token)
        new_tokens = refresh_response.json()

        assert refresh_response.status_code == status.HTTP_200_OK
        assert "access_token" in new_tokens and "refresh_token" in new_tokens

        assert new_tokens["access_token"] != access_token
        assert new_tokens["refresh_token"] != refresh_token

        assert jwt.decode_token(new_tokens["access_token"]) is not None
        assert jwt.decode_token(new_tokens["refresh_token"]) is not None

    def test_refresh_with_access_token(self, user_helper: UserHelper) -> None:
        user_helper.create_default_user()
        login_response = user_helper.login_default_user()
        access_token = login_response.json()["access_token"]

        # refresh token with access token
        refresh_response = user_helper.refresh_user_token(access_token)

        assert refresh_response.status_code == status.HTTP_401_UNAUTHORIZED
