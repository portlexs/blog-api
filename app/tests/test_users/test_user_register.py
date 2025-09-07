from fastapi import status

from tests.helpers.user_helper import UserHelper


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
