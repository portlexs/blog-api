from fastapi import status

from auth import jwt
from tests.helpers.user_helper import UserHelper


class TestRefreshToken:

    def test_successful_refresh_token(self, user_helper: UserHelper) -> None:
        user_helper.default_user.register()
        login_response = user_helper.default_user.login()
        access_token = login_response.json()["access_token"]

        refresh_cookie = login_response.cookies.get("refresh_token")
        assert refresh_cookie is not None

        user_helper.client.cookies.set("refresh_token", refresh_cookie)
        refresh_response = user_helper.refresh_user_token()

        assert refresh_response.status_code == status.HTTP_200_OK
        assert "access_token" in refresh_response.json()

        new_access_token = refresh_response.json()["access_token"]
        assert new_access_token != access_token
        assert jwt.decode_token(new_access_token) is not None
