from fastapi import status

from auth import jwt
from tests.helpers.user_helper import UserHelper


class TestLoginUser:

    def test_successful_login(self, user_helper: UserHelper) -> None:
        user_helper.default_user.register()
        login_response = user_helper.default_user.login()

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
        user_helper.default_user.register()
        login_response = user_helper.login_user(
            user_helper.default_user.email, "wrong_password"
        )

        assert login_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_invalid_email(self, user_helper: UserHelper) -> None:
        login_response = user_helper.login_user("invalid_email", "password123")

        assert login_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_empty_password(self, user_helper: UserHelper) -> None:
        login_response = user_helper.login_user("test_user@example.com", "")

        assert login_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
