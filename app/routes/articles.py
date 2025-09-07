from fastapi import APIRouter, Depends

from services.articles import ArticleService, get_article_service

from schemas.articles import (
    AllArticlesResponse,
    ArticleInfoResponse,
    CreateArticleRequest,
    UpdateArticleRequest,
)


router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/", response_model=AllArticlesResponse)
async def get_articles(
    article_service: ArticleService = Depends(get_article_service),
) -> AllArticlesResponse:
    """Get all articles in blog"""
    return article_service.get_all_articles()


@router.get("/{slug}", response_model=ArticleInfoResponse)
async def get_article(
    slug: str, article_service: ArticleService = Depends(get_article_service)
) -> ArticleInfoResponse:
    """Get article in blog"""
    return article_service.get_article(slug=slug)


@router.post("/", response_model=ArticleInfoResponse)
async def create_article(
    article_in: CreateArticleRequest,
    article_service: ArticleService = Depends(get_article_service),
) -> ArticleInfoResponse:
    """Create article in blog"""
    return article_service.create_article(article_in=article_in)


@router.put("/{slug}", response_model=ArticleInfoResponse)
async def update_article(
    slug: str,
    article_in: UpdateArticleRequest,
    article_service: ArticleService = Depends(get_article_service),
) -> ArticleInfoResponse:
    """Update article in blog"""
    return article_service.update_article(slug=slug, article_in=article_in)


@router.delete("/{slug}")
async def delete_article(
    slug: str, article_service: ArticleService = Depends(get_article_service)
):
    """Delete article in blog"""
    return article_service.delete_article(slug=slug)
