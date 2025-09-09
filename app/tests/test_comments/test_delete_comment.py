import uuid

from fastapi import status

from tests.helpers.article_helper import ArticleHelper
from tests.helpers.comment_helper import CommentHelper
from tests.helpers.user_helper import UserHelper


class TestDeleteComment:
    def test_successful_delete_comment(
        self,
        user_helper: UserHelper,
        article_helper: ArticleHelper,
        comment_helper: CommentHelper,
    ) -> None:
        access_token = user_helper.default_user.register_and_login()
        headers = {"Authorization": f"Bearer {access_token}"}

        create_article_response = article_helper.default_article.create_article(headers)
        article_slug = create_article_response.json()["slug"]

        create_comment_response = comment_helper.default_comment.create_comment(
            article_slug, headers
        )
        comment_id = create_comment_response.json()["id"]

        delete_comment_response = comment_helper.delete_comment(
            article_slug, comment_id, headers
        )

        assert delete_comment_response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_comment_with_unauthorized_user(
        self,
        user_helper: UserHelper,
        article_helper: ArticleHelper,
        comment_helper: CommentHelper,
    ) -> None:
        access_token = user_helper.default_user.register_and_login()
        headers = {"Authorization": f"Bearer {access_token}"}

        create_article_response = article_helper.default_article.create_article(headers)
        article_slug = create_article_response.json()["slug"]

        create_comment_response = comment_helper.default_comment.create_comment(
            article_slug, headers
        )
        comment_id = create_comment_response.json()["id"]

        delete_comment_response = comment_helper.delete_comment(
            article_slug, comment_id, headers={}
        )

        assert delete_comment_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_comment_in_nonexistent_article(
        self,
        user_helper: UserHelper,
        article_helper: ArticleHelper,
        comment_helper: CommentHelper,
    ) -> None:
        access_token = user_helper.default_user.register_and_login()
        headers = {"Authorization": f"Bearer {access_token}"}

        create_article_response = article_helper.default_article.create_article(headers)
        article_slug = create_article_response.json()["slug"]

        create_comment_response = comment_helper.default_comment.create_comment(
            article_slug, headers
        )
        comment_id = create_comment_response.json()["id"]

        delete_comment_response = comment_helper.delete_comment(
            "nonexistent-article", comment_id, headers
        )

        assert delete_comment_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_nonexistent_comment(
        self,
        user_helper: UserHelper,
        article_helper: ArticleHelper,
        comment_helper: CommentHelper,
    ) -> None:
        access_token = user_helper.default_user.register_and_login()
        headers = {"Authorization": f"Bearer {access_token}"}

        create_article_response = article_helper.default_article.create_article(headers)
        article_slug = create_article_response.json()["slug"]

        delete_comment_response = comment_helper.delete_comment(
            article_slug, uuid.uuid4(), headers
        )

        assert delete_comment_response.status_code == status.HTTP_404_NOT_FOUND
