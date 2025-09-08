from typing import Any, Dict

from fastapi.testclient import TestClient
from httpx import Response


class DefaultArticle:
    def __init__(self, client: TestClient) -> None:
        self.client = client
        self.title = "Test Article"
        self.description = "This is a test article."
        self.body = "This is the body of the test article."
        self.tag_list = ["test", "article"]

    def create_article(self, headers: Dict[str, str]) -> Response:
        json = {
            "title": self.title,
            "description": self.description,
            "body": self.body,
            "tag_list": self.tag_list,
        }
        return self.client.post("/api/articles/", headers=headers, json=json)


class ArticleHelper:
    def __init__(self, client: TestClient) -> None:
        self.client = client
        self.default_article = DefaultArticle(client)

    def create_article(
        self, headers: Dict[str, str], article_data: Dict[str, Any]
    ) -> Response:
        return self.client.post("/api/articles/", headers=headers, json=article_data)

    def get_all_articles(self, headers: Dict[str, str]) -> Response:
        return self.client.get("/api/articles/", headers=headers)

    def get_article(self, headers: Dict[str, str], slug: str) -> Response:
        return self.client.get(f"/api/articles/{slug}", headers=headers)

    def update_article(
        self, headers: Dict[str, str], slug: str, article_data: Dict[str, Any]
    ) -> Response:
        return self.client.put(
            f"/api/articles/{slug}", headers=headers, json=article_data
        )

    def delete_article(self, headers: Dict[str, str], slug: str) -> Response:
        return self.client.delete(f"/api/articles/{slug}", headers=headers)
