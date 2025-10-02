from fastapi import APIRouter, Depends, status

from app.schemas.token_schemas import AuthTokens
from app.schemas.user_schemas import (
    PublicUser,
    UserCreate,
    UserLogin,
    UserSearch,
    UserUpdate,
)
from app.services.dependencies import AuthServiceDep, CurrentUserDep, UserServiceDep


router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    path="/me",
    response_model=PublicUser,
    status_code=status.HTTP_200_OK,
)
async def get_current_user(current_user: CurrentUserDep) -> PublicUser:
    return PublicUser.model_validate(current_user)


@router.get(
    path="/search",
    response_model=PublicUser,
    status_code=status.HTTP_200_OK,
)
async def search_user(
    _current_user: CurrentUserDep,
    user_service: UserServiceDep,
    user_in: UserSearch = Depends(),
) -> PublicUser:
    user = await user_service.get_user(user_in)
    return PublicUser.model_validate(user)


@router.post(
    path="/register",
    response_model=AuthTokens,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    auth_service: AuthServiceDep, user_in: UserCreate
) -> AuthTokens:
    access_token, refresh_token = await auth_service.register_user(user_in)
    return AuthTokens(access_token=access_token, refresh_token=refresh_token)


@router.post(
    path="/login",
    response_model=AuthTokens,
    status_code=status.HTTP_200_OK,
)
async def login_user(auth_service: AuthServiceDep, user_in: UserLogin) -> AuthTokens:
    access_token, refresh_token = await auth_service.login_user(user_in)
    return AuthTokens(access_token=access_token, refresh_token=refresh_token)


@router.put(
    path="/me/update",
    response_model=PublicUser,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    current_user: CurrentUserDep, user_service: UserServiceDep, user_in: UserUpdate
) -> PublicUser:
    user = await user_service.update_user(current_user, user_in)
    return PublicUser.model_validate(user)


@router.delete(
    path="/me/delete",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    current_user: CurrentUserDep, user_service: UserServiceDep
) -> None:
    await user_service.delete_user(current_user)


@router.post(
    path="/me/refresh",
    response_model=AuthTokens,
    status_code=status.HTTP_200_OK,
)
async def refresh_tokens(
    current_user: CurrentUserDep, auth_service: AuthServiceDep
) -> AuthTokens:
    access_token, refresh_token = auth_service.refresh_tokens(current_user)
    return AuthTokens(access_token=access_token, refresh_token=refresh_token)
