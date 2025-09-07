from fastapi import status

from tests.helpers.user_helper import UserHelper


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
