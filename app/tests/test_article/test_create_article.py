from http import HTTPStatus

import pytest

from app.tests.clients.artcles_client import ArticleClient
from app.tests.clients.user_client import UserClient


@pytest.mark.asyncio
class TestCreateArticle:
    async def test_successful_create_article(
        self, user_client: UserClient, article_client: ArticleClient
    ) -> None:
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        access_token = register_response.json()["access_token"]

        create_article_response = await article_client.create_article(
            {"title": "test", "body": "test", "description": "test"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert create_article_response.status_code == HTTPStatus.CREATED

    async def test_successful_create_article_with_tag_list(
        self, user_client: UserClient, article_client: ArticleClient
    ) -> None:
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        access_token = register_response.json()["access_token"]

        create_article_response = await article_client.create_article(
            {
                "title": "test",
                "body": "test",
                "description": "test",
                "tagList": ["test1", "test2"],
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert create_article_response.status_code == HTTPStatus.CREATED
