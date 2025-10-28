from http import HTTPStatus

import pytest

from app.tests.clients.artcles_client import ArticleClient
from app.tests.clients.user_client import UserClient
from app.tests.clients.comment_client import CommentClient


@pytest.mark.asyncio
class TestCreateComment:
    async def test_successful_create_comment_in_user_article(
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
        create_comment_response = await comment_client.create_comment(
            article_slug,
            {"body": "This is a test comment."},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert create_comment_response.json()["body"] == "This is a test comment."
        assert create_comment_response.status_code == HTTPStatus.CREATED

    async def test_successful_create_comment_in_another_user_article(
        self,
        user_client: UserClient,
        article_client: ArticleClient,
        comment_client: CommentClient,
    ):
        # register first user
        register_response_1 = await user_client.register_user(
            {
                "username": "test1",
                "email": "email1@example.com",
                "password": "password1",
            }
        )
        access_token_1 = register_response_1.json()["access_token"]

        # register second user
        register_response_2 = await user_client.register_user(
            {
                "username": "test2",
                "email": "email2@example.com",
                "password": "password2",
            }
        )
        access_token_2 = register_response_2.json()["access_token"]

        # create article as first user
        create_article_response = await article_client.create_article(
            {"title": "test", "body": "test", "description": "test"},
            headers={"Authorization": f"Bearer {access_token_1}"},
        )
        article_slug = create_article_response.json()["slug"]

        # create comment as second user
        create_comment_response = await comment_client.create_comment(
            article_slug,
            {"body": "This is a test comment."},
            headers={"Authorization": f"Bearer {access_token_2}"},
        )

        assert create_comment_response.json()["body"] == "This is a test comment."
        assert create_comment_response.status_code == HTTPStatus.CREATED

    async def test_create_comment_unauthorized(
        self,
        article_client: ArticleClient,
        comment_client: CommentClient,
        user_client: UserClient,
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

        # create comment without authorization
        create_comment_response = await comment_client.create_comment(
            article_slug, {"body": "This is a test comment."}
        )

        assert create_comment_response.status_code == HTTPStatus.UNAUTHORIZED

    async def test_create_comment_in_nonexistent_article(
        self,
        user_client: UserClient,
        comment_client: CommentClient,
    ):
        # register user
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        access_token = register_response.json()["access_token"]

        # create comment in nonexistent article
        create_comment_response = await comment_client.create_comment(
            "nonexistent-article-slug",
            {"body": "This is a test comment."},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert create_comment_response.status_code == HTTPStatus.NOT_FOUND

    async def test_create_comment_with_empty_body(
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

        # create comment with empty body
        create_comment_response = await comment_client.create_comment(
            article_slug,
            {"body": ""},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert create_comment_response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
