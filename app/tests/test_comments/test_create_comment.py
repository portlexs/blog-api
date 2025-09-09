from fastapi import status

from tests.helpers.article_helper import ArticleHelper
from tests.helpers.comment_helper import CommentHelper
from tests.helpers.user_helper import UserHelper


class TestCreateComment:
    def test_successful_create_comment(
        self,
        user_helper: UserHelper,
        article_helper: ArticleHelper,
        comment_helper: CommentHelper,
    ) -> None:
        access_token = user_helper.default_user.register_and_login()
        headers = {"Authorization": f"Bearer {access_token}"}

        create_article_response = article_helper.default_article.create_article(headers)
        article_slug = create_article_response.json()["slug"]

        create_response = comment_helper.default_comment.create_comment(
            article_slug, headers
        )

        assert create_response.status_code == status.HTTP_201_CREATED

    def test_create_comment_with_unauthorized_user(
        self,
        user_helper: UserHelper,
        article_helper: ArticleHelper,
        comment_helper: CommentHelper,
    ) -> None:
        access_token = user_helper.default_user.register_and_login()
        headers = {"Authorization": f"Bearer {access_token}"}

        create_article_response = article_helper.default_article.create_article(headers)
        article_slug = create_article_response.json()["slug"]

        create_response = comment_helper.default_comment.create_comment(
            article_slug, headers={}
        )

        assert create_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_comment_in_nonexistent_article(
        self, user_helper: UserHelper, comment_helper: CommentHelper
    ) -> None:
        access_token = user_helper.default_user.register_and_login()
        headers = {"Authorization": f"Bearer {access_token}"}

        create_response = comment_helper.default_comment.create_comment(
            "nonexistent-article", headers
        )

        assert create_response.status_code == status.HTTP_404_NOT_FOUND
