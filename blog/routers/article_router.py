from fastapi import APIRouter, Depends, status


from schemas.article_schemas import (
    AllArticles,
    ArticleCreate,
    ArticleUpdate,
    PublicArticle,
)
from services.dependencies import ArticleServiceDep, CurrentUserDep


router = APIRouter(prefix="/articles", tags=["articles"])


@router.get(
    path="/",
    response_model=AllArticles,
    status_code=status.HTTP_200_OK,
)
async def get_articles(
    current_user: CurrentUserDep,
    article_service: ArticleServiceDep,
) -> AllArticles:
    articles = await article_service.get_all_articles(current_user)
    return AllArticles(articles=articles)


@router.get(
    path="/{article_slug}",
    response_model=PublicArticle,
    status_code=status.HTTP_200_OK,
)
async def get_article(
    article_slug: str,
    current_user: CurrentUserDep,
    article_service: ArticleServiceDep,
) -> PublicArticle:
    article = await article_service.get_article(article_slug, current_user)
    return PublicArticle.model_validate(article)


@router.post(
    path="/",
    response_model=PublicArticle,
    status_code=status.HTTP_201_CREATED,
)
async def create_article(
    current_user: CurrentUserDep,
    article_service: ArticleServiceDep,
    article_in: ArticleCreate,
) -> PublicArticle:
    article = await article_service.create_article(article_in, current_user)
    return PublicArticle.model_validate(article)


@router.put(
    path="/{article_slug}",
    response_model=PublicArticle,
    status_code=status.HTTP_200_OK,
)
async def update_article(
    article_slug: str,
    current_user: CurrentUserDep,
    article_service: ArticleServiceDep,
    article_in: ArticleUpdate,
) -> PublicArticle:
    article = await article_service.update_article(
        article_slug, article_in, current_user
    )
    return PublicArticle.model_validate(article)


@router.delete(
    path="/{article_slug}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_article(
    article_slug: str,
    current_user: CurrentUserDep,
    article_service: ArticleServiceDep,
) -> None:
    await article_service.delete_article(article_slug, current_user)
