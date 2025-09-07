from fastapi import status

from tests.helpers.user_helper import UserHelper


class TestGetUser:

    def test_successful_create_and_get_user(self, user_helper: UserHelper) -> None:
        access_token = user_helper.default_user.register_and_login()

        get_response = user_helper.get_user(
            headers={"Authorization": f"Bearer {access_token}"}
        )

        assert get_response.status_code == status.HTTP_200_OK
        assert "password" not in get_response.json()

    def test_user_unauthorized(self, user_helper: UserHelper) -> None:
        get_response = user_helper.get_user(headers={})

        assert get_response.status_code == status.HTTP_401_UNAUTHORIZED
