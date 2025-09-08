from fastapi import status

from helpers.article_helper import ArticleHelper
from helpers.user_helper import UserHelper


class TestCreateArticle:
    def test_successful_create_with_valid_data(
        self, user_helper: UserHelper, article_helper: ArticleHelper
    ) -> None:
        access_token = user_helper.default_user.register_and_login()

        create_response = article_helper.default_article.create_article(
            headers={"Authorization": f"Bearer {access_token}"}
        )

        assert create_response.status_code == status.HTTP_201_CREATED
        assert "slug" in create_response.json()

    def test_create_with_unauthorized_user(self, article_helper: ArticleHelper) -> None:
        create_response = article_helper.default_article.create_article(headers={})

        assert create_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_creating_slug_exists(
        self, user_helper: UserHelper, article_helper: ArticleHelper
    ) -> None:
        access_token = user_helper.default_user.register_and_login()
        headers = {"Authorization": f"Bearer {access_token}"}

        article_helper.create_article(
            headers=headers,
            article_data={
                "title": "Сила сибири",
                "description": "None",
                "body": "None",
            },
        )

        create_response = article_helper.create_article(
            headers=headers,
            article_data={
                "title": "сиЛа Сибири",
                "description": "None",
                "body": "None",
            },
        )

        assert create_response.status_code == status.HTTP_400_BAD_REQUEST
