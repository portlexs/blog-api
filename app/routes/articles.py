from fastapi import APIRouter

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
)


@router.get("/")
async def get_articles() -> dict:
    """Get all articles in blog"""
    return {"message": "get_articles()"}


@router.get("/{article_id}")
async def get_article(article_id: int) -> dict:
    """Get article in blog by id"""
    return {"message": f"get_article({article_id})"}


@router.post("/")
async def create_article() -> dict:
    """Create article in blog"""
    return {"message": "create_article()"}


@router.put("/{article_id}")
async def update_article(article_id: int) -> dict:
    """Update article in blog by id"""
    return {"message": f"update_article({article_id})"}


@router.delete("/{article_id}")
async def delete_article(article_id: int) -> dict:
    """Delete article in blog by id"""
    return {"message": f"delete_article({article_id})"}
