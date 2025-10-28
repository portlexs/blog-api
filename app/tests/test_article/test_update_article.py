from http import HTTPStatus

import pytest

from app.tests.clients.artcles_client import ArticleClient
from app.tests.clients.user_client import UserClient


@pytest.mark.asyncio
class TestUpdateArticle:
    async def test_successful_update_article(
        self, user_client: UserClient, article_client: ArticleClient
    ) -> None:
        # register user
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        access_token = register_response.json()["access_token"]

        # create an article
        create_article_response = await article_client.create_article(
            {
                "title": "test",
                "body": "test",
                "description": "test",
                "tagList": ["test"],
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )
        article_slug = create_article_response.json()["slug"]

        # update the article
        update_article_response = await article_client.update_article(
            article_slug,
            {
                "title": "test2",
                "body": "test2",
                "description": "test2",
                "tagList": ["test2"],
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert update_article_response.status_code == HTTPStatus.OK

    async def test_update_non_existent_article(
        self, user_client: UserClient, article_client: ArticleClient
    ) -> None:
        # register user
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        access_token = register_response.json()["access_token"]

        # try to update a non-existent article
        update_article_response = await article_client.update_article(
            "non-existent-article-slug",
            {
                "title": "test2",
                "body": "test2",
                "description": "test2",
                "tagList": ["test2"],
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert update_article_response.status_code == HTTPStatus.NOT_FOUND

    async def test_update_article_unauthorized(
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

        # try to update the article without authorization
        update_article_response = await article_client.update_article(article_slug, {})

        assert update_article_response.status_code == HTTPStatus.UNAUTHORIZED

    async def test_update_article_forbidden(
        self, user_client: UserClient, article_client: ArticleClient
    ) -> None:
        # register first user
        register_response_1 = await user_client.register_user(
            {"username": "user1", "email": "email1@example.com", "password": "password"}
        )
        access_token_1 = register_response_1.json()["access_token"]

        # register second user
        register_response_2 = await user_client.register_user(
            {"username": "user2", "email": "email2@example.com", "password": "password"}
        )
        access_token_2 = register_response_2.json()["access_token"]

        # create an article as first user
        create_article_response = await article_client.create_article(
            {"title": "test", "body": "test", "description": "test"},
            headers={"Authorization": f"Bearer {access_token_1}"},
        )
        article_slug = create_article_response.json()["slug"]

        # try to update the article as second user
        update_article_response = await article_client.update_article(
            article_slug,
            {},
            headers={"Authorization": f"Bearer {access_token_2}"},
        )

        assert update_article_response.status_code == HTTPStatus.NOT_FOUND

    async def test_update_article_with_existing_slug(
        self, user_client: UserClient, article_client: ArticleClient
    ) -> None:
        # register user
        register_response = await user_client.register_user(
            {"username": "test", "email": "email@example.com", "password": "password"}
        )
        access_token = register_response.json()["access_token"]

        # create an article
        create_article_response_1 = await article_client.create_article(
            {"title": "test1", "body": "test", "description": "test"},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        article_slug_1 = create_article_response_1.json()["slug"]

        # create another article with the same slug
        create_article_response_2 = await article_client.create_article(
            {"title": "test2", "body": "test", "description": "test"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        # try to update the first article to have the same slug as the second article
        update_article_response = await article_client.update_article(
            article_slug_1,
            {"title": "test2", "body": "test", "description": "test"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert update_article_response.status_code == HTTPStatus.CONFLICT
