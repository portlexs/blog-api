from typing import Dict

from httpx import AsyncClient, Response


class CommentClient:
    def __init__(self, client: AsyncClient) -> None:
        self.client = client

    async def get_comments(
        self, article_slug: str, headers: Dict | None = None
    ) -> Response:
        return await self.client.get(
            f"/api/articles/{article_slug}/comments/", headers=headers
        )

    async def create_comment(
        self, article_slug: str, comment_in: Dict, headers: Dict | None = None
    ) -> Response:
        return await self.client.post(
            f"/api/articles/{article_slug}/comments/", json=comment_in, headers=headers
        )

    async def update_comment(
        self,
        article_slug: str,
        comment_id: str,
        comment_in: Dict,
        headers: Dict | None = None,
    ) -> Response:
        return await self.client.post(
            f"/api/articles/{article_slug}/comments/{comment_id}",
            json=comment_in,
            headers=headers,
        )

    async def delete_comment(
        self, article_slug: str, comment_id: str, headers: Dict | None = None
    ) -> Response:
        return await self.client.delete(
            f"/api/articles/{article_slug}/comments/{comment_id}", headers=headers
        )
