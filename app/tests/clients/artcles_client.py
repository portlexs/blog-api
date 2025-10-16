from typing import Dict, Optional

from httpx import AsyncClient, Response


class ArticleClient:
    def __init__(self, client: AsyncClient) -> None:
        self.client = client
        self.base_url = "/api/articles"

    async def get_user_articles(self, headers: Optional[Dict]) -> Response:
        return await self.client.get(f"{self.base_url}/", headers=headers)

    async def get_user_article(
        self, article_slug: int, headers: Optional[Dict]
    ) -> Response:
        return await self.client.get(f"{self.base_url}/{article_slug}", headers=headers)

    async def create_article(
        self, article_in: Dict, headers: Optional[Dict]
    ) -> Response:
        return await self.client.post(
            f"{self.base_url}/", json=article_in, headers=headers
        )

    async def update_article(
        self, article_slug: str, article_in: Dict, headers: Optional[Dict]
    ) -> Response:
        return await self.client.put(
            f"{self.base_url}/{article_slug}", json=article_in, headers=headers
        )

    async def delete_article(
        self, article_slug: str, headers: Optional[Dict]
    ) -> Response:
        return await self.client.delete(
            f"{self.base_url}/{article_slug}", headers=headers
        )
