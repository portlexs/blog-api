from typing import Any, Dict

from fastapi.testclient import TestClient
from httpx import Response


class DefaultComment:
    def __init__(self, client: TestClient) -> None:
        self.client = client
        self.body = "This is a test comment."

    def create(self, article_slug: str, headers: Dict[str, str]) -> Response:
        comment_data = {"body": self.body}
        return self.client.post(
            f"/api/articles/{article_slug}/comments",
            json=comment_data,
            headers=headers,
        )


class CommentHelper:
    def __init__(self, client: TestClient) -> None:
        self.client = client
        self.default_comment = DefaultComment(client)

    def get_comments(self, article_slug: str, headers: Dict[str, str]) -> Response:
        return self.client.get(
            f"/api/articles/{article_slug}/comments", headers=headers
        )

    def create_comment(
        self, article_slug: str, comment_data: Dict[str, Any], headers: Dict[str, str]
    ) -> Response:
        return self.client.post(
            f"/api/articles/{article_slug}/comments",
            json=comment_data,
            headers=headers,
        )

    def delete_comment(
        self, article_slug: str, comment_id: str, headers: Dict[str, str]
    ):
        return self.client.delete(
            f"/api/articles/{article_slug}/comments/{comment_id}", headers=headers
        )
