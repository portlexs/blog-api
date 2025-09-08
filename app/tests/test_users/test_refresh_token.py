from fastapi import status

from auth import jwt
from tests.helpers.user_helper import UserHelper


class TestRefreshToken:

    def test_successful_refresh_token(self, user_helper: UserHelper) -> None:
        user_helper.default_user.register()

        login_response = user_helper.default_user.login()
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
        access_token = user_helper.default_user.register_and_login()

        refresh_response = user_helper.refresh_user_token(access_token)

        assert refresh_response.status_code == status.HTTP_401_UNAUTHORIZED
