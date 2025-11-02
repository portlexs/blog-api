import uuid

from fastapi import APIRouter, status

from ..schemas.comment_schemas import (
    CommentCreate,
    CommentUpdate,
    GetCommentsResponse,
    PublicComment,
)
from ..services.dependencies import CurrentUserDep, CommentServiceDep


router = APIRouter(prefix="/articles/{article_slug}/comments", tags=["comments"])


@router.get(
    "/",
    response_model=GetCommentsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_article_comments(
    article_slug: str,
    comment_service: CommentServiceDep,
) -> GetCommentsResponse:
    comments = await comment_service.get_article_comments(article_slug)
    return GetCommentsResponse(comments=comments)


@router.post(
    "/",
    response_model=PublicComment,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    article_slug: str,
    comment_in: CommentCreate,
    current_user: CurrentUserDep,
    comment_service: CommentServiceDep,
) -> PublicComment:
    comment = await comment_service.create_comment(
        article_slug, comment_in, current_user.id
    )
    return PublicComment.model_validate(comment)


@router.post(
    "/{comment_id}",
    response_model=PublicComment,
    status_code=status.HTTP_200_OK,
)
async def update_comment(
    article_slug: str,
    comment_id: uuid.UUID,
    comment_in: CommentUpdate,
    current_user: CurrentUserDep,
    comment_service: CommentServiceDep,
) -> PublicComment:
    comment = await comment_service.update_comment(
        article_slug, comment_id, comment_in, current_user.id
    )
    return PublicComment.model_validate(comment)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    article_slug: str,
    comment_id: uuid.UUID,
    current_user: CurrentUserDep,
    comment_service: CommentServiceDep,
) -> None:
    await comment_service.delete_comment(article_slug, comment_id, current_user.id)
