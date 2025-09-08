from fastapi import status

from helpers.article_helper import ArticleHelper
from helpers.user_helper import UserHelper


class TestGetArticle:

    def test_successful_get_all_articles(
        self, user_helper: UserHelper, article_helper: ArticleHelper
    ) -> None:
        access_token = user_helper.default_user.register_and_login()
        headers = {"Authorization": f"Bearer {access_token}"}

        article_helper.default_article.create_article(headers)
        get_response = article_helper.get_all_articles(headers)

        assert get_response.status_code == status.HTTP_200_OK

    def test_successful_get_article_by_slug(
        self, user_helper: UserHelper, article_helper: ArticleHelper
    ) -> None:
        access_token = user_helper.default_user.register_and_login()
        headers = {"Authorization": f"Bearer {access_token}"}

        create_response = article_helper.default_article.create_article(headers)
        slug = create_response.json()["slug"]

        get_response = article_helper.get_article(headers, slug)

        assert get_response.status_code == status.HTTP_200_OK

    def test_get_all_articles_with_unauthorized_user(
        self, article_helper: ArticleHelper
    ) -> None:
        get_response = article_helper.get_all_articles(headers={})

        assert get_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_article_with_unauthorized_user(
        self, user_helper: UserHelper, article_helper: ArticleHelper
    ) -> None:
        access_token = user_helper.default_user.register_and_login()
        headers = {"Authorization": f"Bearer {access_token}"}

        create_response = article_helper.default_article.create_article(headers)
        slug = create_response.json()["slug"]

        get_response = article_helper.get_article(headers={}, slug=slug)

        assert get_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_article_with_invalid_slug(
        self, user_helper: UserHelper, article_helper: ArticleHelper
    ) -> None:
        access_token = user_helper.default_user.register_and_login()
        headers = {"Authorization": f"Bearer {access_token}"}

        get_response = article_helper.get_article(headers, "invalid_slug")

        assert get_response.status_code == status.HTTP_404_NOT_FOUND
