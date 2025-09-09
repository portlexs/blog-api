from fastapi import status

from tests.helpers.article_helper import ArticleHelper
from tests.helpers.comment_helper import CommentHelper
from tests.helpers.user_helper import UserHelper


class TestGetComment:
    def test_successful_get_comments(
        self,
        user_helper: UserHelper,
        article_helper: ArticleHelper,
        comment_helper: CommentHelper,
    ) -> None:
        access_token = user_helper.default_user.register_and_login()
        headers = {"Authorization": f"Bearer {access_token}"}

        create_article_response = article_helper.default_article.create_article(headers)
        article_slug = create_article_response.json()["slug"]

        comment_helper.default_comment.create_comment(article_slug, headers)
        get_comments_response = comment_helper.get_comments(article_slug, headers)

        assert get_comments_response.status_code == status.HTTP_200_OK
        assert len(get_comments_response.json()["comments"]) == 1

    def test_get_comments_with_unauthorized_user(
        self,
        user_helper: UserHelper,
        article_helper: ArticleHelper,
        comment_helper: CommentHelper,
    ) -> None:
        access_token = user_helper.default_user.register_and_login()
        headers = {"Authorization": f"Bearer {access_token}"}

        create_article_response = article_helper.default_article.create_article(headers)
        article_slug = create_article_response.json()["slug"]

        get_comments_response = comment_helper.get_comments(article_slug, headers={})

        assert get_comments_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_comments_in_nonexistent_article(
        self, user_helper: UserHelper, comment_helper: CommentHelper
    ) -> None:
        access_token = user_helper.default_user.register_and_login()
        headers = {"Authorization": f"Bearer {access_token}"}

        get_comments_response = comment_helper.get_comments(
            "nonexistent-article", headers
        )

        assert get_comments_response.status_code == status.HTTP_404_NOT_FOUND
