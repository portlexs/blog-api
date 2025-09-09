import uuid

from fastapi import APIRouter, Depends, status

from auth.dependencies import CurrentUser
from schemas.comments import (
    CommentCreate,
    CommentInfoResponse,
    GetCommentsResponse,
)
from services.comments import CommentService, get_comment_service


router = APIRouter(prefix="/articles/{article_slug}/comments", tags=["comments"])


@router.get(
    "/",
    response_model=GetCommentsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_comments(
    article_slug: str,
    user: CurrentUser,
    comment_service: CommentService = Depends(get_comment_service),
) -> GetCommentsResponse:
    """Get comments list from article"""
    comments = comment_service.get_artile_comments(article_slug=article_slug)
    return GetCommentsResponse(comments=comments)


@router.post(
    "/",
    response_model=CommentInfoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    article_slug: str,
    comment_in: CommentCreate,
    user: CurrentUser,
    comment_service: CommentService = Depends(get_comment_service),
) -> CommentInfoResponse:
    """Create comment in article"""
    comment = comment_service.create_comment(article_slug, comment_in, user)
    return CommentInfoResponse.model_validate(comment, mode="json")


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comments(
    article_slug: str,
    comment_id: uuid.UUID,
    user: CurrentUser,
    comment_service: CommentService = Depends(get_comment_service),
) -> None:
    """Delete comment in article"""
    comment_service.delete_comment(article_slug, comment_id)
