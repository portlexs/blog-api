from fastapi import status

from core import jwt
from tests.helpers.user_helper import UserHelper


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
