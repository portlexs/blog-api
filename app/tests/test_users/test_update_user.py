from fastapi import status

from tests.helpers.user_helper import UserHelper


class TestUpdateUser:

    def test_successful_update_user_email(self, user_helper: UserHelper) -> None:
        access_token = user_helper.default_user.register_and_login()

        user_data_to_update = {"email": "new_test_user@example.com"}
        update_response = user_helper.update_user(
            headers={"Authorization": f"Bearer {access_token}"},
            user_data=user_data_to_update,
        )

        assert update_response.status_code == status.HTTP_200_OK

        # login user with new email
        login_response = user_helper.login_user(
            "new_test_user@example.com", user_helper.default_user.password
        )

        assert login_response.status_code == status.HTTP_200_OK

    def test_successful_update_user_password(self, user_helper: UserHelper) -> None:
        access_token = user_helper.default_user.register_and_login()

        # update user password
        user_data_to_update = {"password": "new_password123"}
        update_response = user_helper.update_user(
            headers={"Authorization": f"Bearer {access_token}"},
            user_data=user_data_to_update,
        )

        assert update_response.status_code == status.HTTP_200_OK

        # login user with new password
        login_response = user_helper.login_user(
            user_helper.default_user.email, "new_password123"
        )

        assert login_response.status_code == status.HTTP_200_OK

    def test_successful_update_user_bio(self, user_helper: UserHelper) -> None:
        access_token = user_helper.default_user.register_and_login()

        user_data_to_update = {"bio": "new_bio"}
        update_response = user_helper.update_user(
            headers={"Authorization": f"Bearer {access_token}"},
            user_data=user_data_to_update,
        )

        assert update_response.status_code == status.HTTP_200_OK

    def test_successful_update_user_image_url(self, user_helper: UserHelper) -> None:
        access_token = user_helper.default_user.register_and_login()

        user_data_to_update = {"image_url": "https://example.com/new_image.jpg"}
        update_response = user_helper.update_user(
            headers={"Authorization": f"Bearer {access_token}"},
            user_data=user_data_to_update,
        )

        assert update_response.status_code == status.HTTP_200_OK

    def test_updating_user_unauthorized(self, user_helper: UserHelper) -> None:
        user_data = {"email": "test_user@example.com", "password": "password123"}

        update_response = user_helper.update_user(
            headers={"Authorization": "Bearer invalid_token"},
            user_data=user_data,
        )

        assert update_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_updating_email_already_exists(self, user_helper: UserHelper) -> None:
        access_token = user_helper.default_user.register_and_login()

        # try to update user email
        user_data_to_update = {"email": user_helper.default_user.email}
        update_response = user_helper.update_user(
            headers={"Authorization": f"Bearer {access_token}"},
            user_data=user_data_to_update,
        )

        assert update_response.status_code == status.HTTP_400_BAD_REQUEST

    def test_updating_username_already_exists(self, user_helper: UserHelper) -> None:
        access_token = user_helper.default_user.register_and_login()

        # try to update user username
        user_data_to_update = {"username": user_helper.default_user.username}
        update_response = user_helper.update_user(
            headers={"Authorization": f"Bearer {access_token}"},
            user_data=user_data_to_update,
        )

        assert update_response.status_code == status.HTTP_400_BAD_REQUEST
