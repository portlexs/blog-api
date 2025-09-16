from typing import Annotated

from fastapi import APIRouter, Depends, status

from users.user_service import UserService
from users.user_schemas import UserCreate, PublicUser

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    path="/register",
    response_model=PublicUser,
    status_code=status.HTTP_200_OK,
)
async def register_user(
    user_in: UserCreate, service: Annotated[UserService, Depends()]
) -> PublicUser:
    user = await service.create_user(user_in)
    return PublicUser.model_validate(user)
