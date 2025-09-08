from fastapi import APIRouter, Depends

from services.articles import ArticleService, get_article_service

from core.auth_dependencies import CurrentUser
from schemas.articles import (
    AllArticlesResponse,
    ArticleInfoResponse,
    ArticleCreate,
    ArticleUpdate,
)


router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/", response_model=AllArticlesResponse, status_code=200)
async def get_articles(
    current_user: CurrentUser,
    article_service: ArticleService = Depends(get_article_service),
) -> AllArticlesResponse:
    """Get all articles in blog"""
    articles = article_service.get_all_articles(current_user)
    return AllArticlesResponse(articles=articles)


@router.get("/{slug}", response_model=ArticleInfoResponse, status_code=200)
async def get_article(
    current_user: CurrentUser,
    slug: str,
    article_service: ArticleService = Depends(get_article_service),
) -> ArticleInfoResponse:
    """Get article in blog"""
    article = article_service.get_article(slug=slug, user_id=current_user.id)
    return ArticleInfoResponse.model_validate(article)


@router.post("/", response_model=ArticleInfoResponse, status_code=201)
async def create_article(
    current_user: CurrentUser,
    article_in: ArticleCreate,
    article_service: ArticleService = Depends(get_article_service),
) -> ArticleInfoResponse:
    """Create article in blog"""
    article = article_service.create_article(article_in, current_user)
    return ArticleInfoResponse.model_validate(article)


@router.put("/{slug}", response_model=ArticleInfoResponse, status_code=200)
async def update_article(
    current_user: CurrentUser,
    slug: str,
    article_in: ArticleUpdate,
    article_service: ArticleService = Depends(get_article_service),
) -> ArticleInfoResponse:
    """Update article in blog"""
    article = article_service.update_article(
        slug=slug, article_in=article_in, user=current_user
    )
    return ArticleInfoResponse.model_validate(article)


@router.delete("/{slug}", response_model=dict, status_code=200)
async def delete_article(
    current_user: CurrentUser,
    slug: str,
    article_service: ArticleService = Depends(get_article_service),
):
    """Delete article in blog"""
    article_service.delete_article(slug=slug, user=current_user)
    return {"message": f"delete_article {slug}"}
