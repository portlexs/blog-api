from http import HTTPStatus

import pytest

from app.tests.clients.artcles_client import ArticleClient
from app.tests.clients.user_client import UserClient


@pytest.mark.asyncio
class TestGetArticle:
    async def test_successful_get_current_user_article(
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

        # get the article
        get_article_response = await article_client.get_article(
            article_slug,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert get_article_response.status_code == HTTPStatus.OK

    async def test_get_another_user_article(
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

        # get the article as second user
        get_article_response = await article_client.get_article(
            article_slug,
            headers={"Authorization": f"Bearer {access_token_user2}"},
        )

        assert get_article_response.status_code == HTTPStatus.OK
