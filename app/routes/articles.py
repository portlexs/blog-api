from fastapi import APIRouter, Depends

from services.articles import ArticleService, get_article_service


router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/")
async def get_articles(article_service: ArticleService = Depends(get_article_service)):
    """Get all articles in blog"""
    return article_service.get_all_articles()


@router.get("/{slug}")
async def get_article(
    slug: str, article_service: ArticleService = Depends(get_article_service)
):
    """Get article in blog"""
    return article_service.get_article(slug=slug)


@router.post("/")
async def create_article(
    article_in,
    article_service: ArticleService = Depends(get_article_service),
):
    """Create article in blog"""
    return article_service.create_article(article_in=article_in)


@router.put("/{slug}")
async def update_article(
    slug: str,
    article_in,
    article_service: ArticleService = Depends(get_article_service),
):
    """Update article in blog"""
    return article_service.update_article(slug=slug, article_in=article_in)


@router.delete("/{slug}")
async def delete_article(
    slug: str, article_service: ArticleService = Depends(get_article_service)
):
    """Delete article in blog"""
    return article_service.delete_article(slug=slug)
