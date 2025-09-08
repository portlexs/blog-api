from fastapi import status

from helpers.article_helper import ArticleHelper
from helpers.user_helper import UserHelper


class TestDeleteArticle:
    def test_successful_delete_article_by_slug(
        self, user_helper: UserHelper, article_helper: ArticleHelper
    ) -> None:
        access_token = user_helper.default_user.register_and_login()
        headers = {"Authorization": f"Bearer {access_token}"}

        create_response = article_helper.default_article.create_article(headers)
        slug = create_response.json()["slug"]

        delete_response = article_helper.delete_article(headers, slug)

        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_article_with_unauthorized_user(
        self, user_helper: UserHelper, article_helper: ArticleHelper
    ) -> None:
        access_token = user_helper.default_user.register_and_login()
        headers = {"Authorization": f"Bearer {access_token}"}

        create_response = article_helper.default_article.create_article(headers)
        slug = create_response.json()["slug"]

        delete_response = article_helper.delete_article(headers={}, slug=slug)

        assert delete_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_article_with_invalid_slug(
        self, user_helper: UserHelper, article_helper: ArticleHelper
    ) -> None:
        access_token = user_helper.default_user.register_and_login()
        headers = {"Authorization": f"Bearer {access_token}"}

        delete_response = article_helper.delete_article(headers, "invalid_slug")

        assert delete_response.status_code == status.HTTP_404_NOT_FOUND
