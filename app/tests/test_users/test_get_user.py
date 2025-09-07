from fastapi import status

from tests.helpers.user_helper import UserHelper


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
