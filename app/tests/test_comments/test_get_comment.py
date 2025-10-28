from http import HTTPStatus

import pytest

from app.tests.clients.artcles_client import ArticleClient
from app.tests.clients.user_client import UserClient
from app.tests.clients.comment_client import CommentClient


@pytest.mark.asyncio
class TestGetComment:
    async def test_successful_get_article_comments(
        self,
        user_client: UserClient,
        article_client: ArticleClient,
        comment_client: CommentClient,
    ):
        # register user
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        access_token = register_response.json()["access_token"]

        # create article
        create_article_response = await article_client.create_article(
            {"title": "test", "body": "test", "description": "test"},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        article_slug = create_article_response.json()["slug"]

        # create comment
        await comment_client.create_comment(
            article_slug,
            {"body": "This is a test comment."},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        # get comments
        get_comments_response = await comment_client.get_comments(article_slug)

        assert get_comments_response.status_code == HTTPStatus.OK

        comments = get_comments_response.json()["comments"]
        assert len(comments) == 1

    async def test_get_comments_of_non_existent_article(
        self,
        comment_client: CommentClient,
    ):
        # get comments
        get_comments_response = await comment_client.get_comments(
            "non-existent-article"
        )

        assert get_comments_response.status_code == HTTPStatus.NOT_FOUND

    async def test_get_comments_when_no_comments_exist(
        self,
        user_client: UserClient,
        article_client: ArticleClient,
        comment_client: CommentClient,
    ):
        # register user
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        access_token = register_response.json()["access_token"]

        # create article
        create_article_response = await article_client.create_article(
            {"title": "test", "body": "test", "description": "test"},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        article_slug = create_article_response.json()["slug"]

        # get comments
        get_comments_response = await comment_client.get_comments(article_slug)

        assert get_comments_response.status_code == HTTPStatus.OK

        comments = get_comments_response.json()["comments"]
        assert len(comments) == 0
