import uuid
from http import HTTPStatus

import pytest

from app.tests.clients.artcles_client import ArticleClient
from app.tests.clients.user_client import UserClient
from app.tests.clients.comment_client import CommentClient


@pytest.mark.asyncio
class TestUpdateComment:
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
        comment_id = create_comment_response.json()["id"]

        # update comment
        update_comment_response = await comment_client.update_comment(
            article_slug,
            comment_id,
            {"body": "This is an updated test comment."},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert update_comment_response.status_code == HTTPStatus.OK
        assert (
            update_comment_response.json()["body"] == "This is an updated test comment."
        )

    async def test_update_comment_not_found(
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

        # update non-existing comment
        update_comment_response = await comment_client.update_comment(
            article_slug,
            str(uuid.uuid4()),
            {"body": "This is an updated test comment."},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert update_comment_response.status_code == HTTPStatus.NOT_FOUND

    async def test_update_comment_unauthorized(
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
        comment_id = create_comment_response.json()["id"]

        # update comment without authorization
        update_comment_response = await comment_client.update_comment(
            article_slug, comment_id, {"body": "This is an updated test comment."}
        )

        assert update_comment_response.status_code == HTTPStatus.UNAUTHORIZED

    async def test_update_comment_of_another_user(
        self,
        user_client: UserClient,
        article_client: ArticleClient,
        comment_client: CommentClient,
    ):
        # register first user
        register_response_1 = await user_client.register_user(
            {
                "username": "user1",
                "email": "email@example.com",
                "password": "password",
            }
        )
        access_token_1 = register_response_1.json()["access_token"]

        # register second user
        register_response_2 = await user_client.register_user(
            {
                "username": "user2",
                "email": "email2@example.com",
                "password": "password",
            }
        )
        access_token_2 = register_response_2.json()["access_token"]

        # create article
        create_article_response = await article_client.create_article(
            {"title": "test", "body": "test", "description": "test"},
            headers={"Authorization": f"Bearer {access_token_1}"},
        )
        article_slug = create_article_response.json()["slug"]

        # create comment
        create_comment_response = await comment_client.create_comment(
            article_slug,
            {"body": "This is a test comment."},
            headers={"Authorization": f"Bearer {access_token_1}"},
        )
        comment_id = create_comment_response.json()["id"]

        # second user tries to update first user's comment
        update_comment_response = await comment_client.update_comment(
            article_slug,
            comment_id,
            {"body": "This is an updated test comment."},
            headers={"Authorization": f"Bearer {access_token_2}"},
        )

        assert update_comment_response.status_code == HTTPStatus.NOT_FOUND
