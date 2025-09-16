from fastapi import APIRouter, Depends, status

from schemas.user_schemas import UserCreate, PublicUser
from services.dependencies import UserServiceDep


router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    path="/register",
    response_model=PublicUser,
    status_code=status.HTTP_200_OK,
)
async def register_user(
    service: UserServiceDep, user_in: UserCreate = Depends()
) -> PublicUser:
    user = await service.create_user(user_in)
    return PublicUser.model_validate(user)
