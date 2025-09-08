from fastapi import APIRouter, Depends

from services.articles import ArticleService, get_article_service

from schemas.articles import (
    AllArticlesResponse,
    ArticleInfoResponse,
    ArticleCreate,
    ArticleUpdate,
)


router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/", response_model=AllArticlesResponse)
async def get_articles(
    article_service: ArticleService = Depends(get_article_service),
) -> AllArticlesResponse:
    """Get all articles in blog"""
    articles = article_service.get_all_articles()
    return AllArticlesResponse(articles=articles)


@router.get("/{slug}", response_model=ArticleInfoResponse)
async def get_article(
    slug: str, article_service: ArticleService = Depends(get_article_service)
) -> ArticleInfoResponse:
    """Get article in blog"""
    article = article_service.get_article(slug=slug)
    return ArticleInfoResponse.model_validate(article)


@router.post("/", response_model=ArticleInfoResponse)
async def create_article(
    article_in: ArticleCreate,
    article_service: ArticleService = Depends(get_article_service),
) -> ArticleInfoResponse:
    """Create article in blog"""
    article = article_service.create_article(article_in=article_in)
    return ArticleInfoResponse.model_validate(article)


@router.put("/{slug}", response_model=ArticleInfoResponse)
async def update_article(
    slug: str,
    article_in: ArticleUpdate,
    article_service: ArticleService = Depends(get_article_service),
) -> ArticleInfoResponse:
    """Update article in blog"""
    article = article_service.update_article(slug=slug, article_in=article_in)
    return ArticleInfoResponse.model_validate(article)


@router.delete("/{slug}")
async def delete_article(
    slug: str, article_service: ArticleService = Depends(get_article_service)
):
    """Delete article in blog"""
    article_service.delete_article(slug=slug)
    return {"message": f"delete_article({slug})"}
