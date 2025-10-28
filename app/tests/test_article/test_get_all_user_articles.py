from http import HTTPStatus

import pytest

from app.tests.clients.artcles_client import ArticleClient
from app.tests.clients.user_client import UserClient


@pytest.mark.asyncio
class TestGetAllUserArticles:
    async def test_successful_get_all_user_articles(
        self, user_client: UserClient, article_client: ArticleClient
    ) -> None:
        # register user
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        access_token = register_response.json()["access_token"]

        # create first article
        await article_client.create_article(
            {"title": "test1", "body": "test1", "description": "test1"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        # create second article
        await article_client.create_article(
            {"title": "test2", "body": "test2", "description": "test2"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        # get all articles for the user
        get_articles_response = await article_client.get_all_user_articles(
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert get_articles_response.status_code == HTTPStatus.OK
        assert len(get_articles_response.json()["articles"]) == 2
