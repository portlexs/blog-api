from fastapi import status

from tests.helpers.user_helper import UserHelper


class TestRegisterUser:

    def test_successful_register(self, user_helper: UserHelper) -> None:
        create_response = user_helper.default_user.register()

        assert create_response.status_code == status.HTTP_201_CREATED

    def test_email_exists(self, user_helper: UserHelper) -> None:
        user_helper.default_user.register()
        create_response = user_helper.default_user.register()

        assert create_response.status_code == status.HTTP_400_BAD_REQUEST

    def test_invalid_email(self, user_helper: UserHelper) -> None:
        user_data = {"email": "invalid_email", "password": "password123"}
        create_response = user_helper.register_user(user_data)

        assert create_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_empty_email(self, user_helper: UserHelper) -> None:
        user_data1 = {"email": "", "password": "password123"}
        create_response1 = user_helper.register_user(user_data1)
        assert create_response1.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        user_data2 = {"email": None, "password": "password123"}
        create_response2 = user_helper.register_user(user_data2)
        assert create_response2.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_empty_password(self, user_helper: UserHelper) -> None:
        user_data = {"email": "test_user@example.com", "password": ""}
        create_response = user_helper.register_user(user_data)

        assert create_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
