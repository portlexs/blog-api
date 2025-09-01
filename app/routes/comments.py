from fastapi import APIRouter

router = APIRouter(
    prefix="/{article_id}/comments",
    tags=["comments"],
)


@router.get("/")
async def get_comments(article_id: int) -> dict:
    """Get comments list in article"""
    return {"message": f"get_comments({article_id})"}


@router.post("/")
async def create_comment(article_id: int) -> dict:
    """Create comment in article"""
    return {"message": f"create_comment({article_id})"}


@router.delete("/{comment_id}")
async def delete_comments(article_id: int, comment_id: int) -> dict:
    """Delete comment in article"""
    return {"message": f"delete_comments({article_id}/{comment_id})"}
