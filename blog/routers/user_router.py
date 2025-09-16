from fastapi import APIRouter, Depends, status

from auth.dependencies import CurrentUserDep
from schemas.user_schemas import PublicUser, UserCreate, UserSearch
from services.dependencies import UserServiceDep


router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    path="/me",
    response_model=PublicUser,
    status_code=status.HTTP_200_OK,
)
async def get_current_user(user: CurrentUserDep) -> PublicUser:
    return PublicUser.model_validate(user)


@router.get(
    path="/search",
    response_model=PublicUser,
    status_code=status.HTTP_200_OK,
)
async def search_user(
    _user: CurrentUserDep, user_service: UserServiceDep, user_in: UserSearch = Depends()
) -> PublicUser:
    user = await user_service.get_user(user_in)
    return PublicUser.model_validate(user)


@router.post(
    path="/register",
    response_model=PublicUser,
    status_code=status.HTTP_200_OK,
)
async def register_user(
    user_service: UserServiceDep, user_in: UserCreate = Depends()
) -> PublicUser:
    user = await user_service.create_user(user_in)
    return PublicUser.model_validate(user)
