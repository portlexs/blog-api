from typing import Annotated

from fastapi import APIRouter, Depends, status

from users.dependencies import get_user_service
from users.user_schemas import UserCreate, PublicUser
from users.user_service import UserService


router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    path="/register",
    response_model=PublicUser,
    status_code=status.HTTP_200_OK,
)
async def register_user(
    service: Annotated[UserService, Depends(get_user_service)],
    user_in: UserCreate = Depends(),
) -> PublicUser:
    user = await service.create_user(user_in)
    return PublicUser.model_validate(user)
