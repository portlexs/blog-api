from http import HTTPStatus

import pytest

from app.tests.clients.artcles_client import ArticleClient
from app.tests.clients.user_client import UserClient


@pytest.mark.asyncio
class TestDeleteArticle:
    async def test_successful_delete_article(
        self, user_client: UserClient, article_client: ArticleClient
    ) -> None:
        # register user
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        access_token = register_response.json()["access_token"]

        # create an article
        create_article_response = await article_client.create_article(
            {"title": "test", "body": "test", "description": "test"},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        article_slug = create_article_response.json()["slug"]

        # delete the article
        delete_article_response = await article_client.delete_article(
            article_slug,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert delete_article_response.status_code == HTTPStatus.NO_CONTENT

        # try to get the deleted article
        get_article_response = await article_client.get_article(
            article_slug,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert get_article_response.status_code == HTTPStatus.NOT_FOUND

    async def test_delete_non_existent_article(
        self, user_client: UserClient, article_client: ArticleClient
    ) -> None:
        # register user
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        access_token = register_response.json()["access_token"]

        # try to delete a non-existent article
        delete_article_response = await article_client.delete_article(
            "non-existent-article-slug",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert delete_article_response.status_code == HTTPStatus.NOT_FOUND

    async def test_delete_article_unauthorized(
        self, user_client: UserClient, article_client: ArticleClient
    ) -> None:
        # register user
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        access_token = register_response.json()["access_token"]

        # create an article
        create_article_response = await article_client.create_article(
            {"title": "test", "body": "test", "description": "test"},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        article_slug = create_article_response.json()["slug"]

        # try to delete an article without authentication
        delete_article_response = await article_client.delete_article(article_slug)

        assert delete_article_response.status_code == HTTPStatus.UNAUTHORIZED

    async def test_delete_another_user_article(
        self, user_client: UserClient, article_client: ArticleClient
    ) -> None:
        # register first user
        register_response_user1 = await user_client.register_user(
            {"username": "user1", "email": "email1@example.com", "password": "password"}
        )
        access_token_user1 = register_response_user1.json()["access_token"]

        # create an article
        create_article_response = await article_client.create_article(
            {"title": "test", "body": "test", "description": "test"},
            headers={"Authorization": f"Bearer {access_token_user1}"},
        )
        article_slug = create_article_response.json()["slug"]

        # register second user
        register_response_user2 = await user_client.register_user(
            {"username": "user2", "email": "email2@example.com", "password": "password"}
        )
        access_token_user2 = register_response_user2.json()["access_token"]

        # try to delete the article as second user
        delete_article_response = await article_client.delete_article(
            article_slug,
            headers={"Authorization": f"Bearer {access_token_user2}"},
        )

        assert delete_article_response.status_code == HTTPStatus.NOT_FOUND
