from fastapi import APIRouter, Cookie, Depends, Response, status

from ..schemas.token_schemas import AuthTokens
from ..schemas.user_schemas import (
    UserCreate,
    UserCurrent,
    UserLogin,
    UserPublic,
    UserSearch,
    UserUpdate,
)
from ..services.dependencies import AuthServiceDep, CurrentUserDep, UserServiceDep
from ..utils.http_responses import set_refresh_token_cookie

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    path="/me",
    response_model=UserCurrent,
    status_code=status.HTTP_200_OK,
)
async def get_current_user(current_user: CurrentUserDep) -> UserCurrent:
    return UserCurrent.model_validate(current_user)


@router.get(
    path="/search",
    response_model=UserPublic,
    status_code=status.HTTP_200_OK,
)
async def search_user(
    _current_user: CurrentUserDep,
    user_service: UserServiceDep,
    user_in: UserSearch = Depends(),
) -> UserPublic:
    user = await user_service.get_user(user_in)
    return UserPublic.model_validate(user)


@router.post(
    path="/register",
    response_model=AuthTokens,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    auth_service: AuthServiceDep, user_in: UserCreate, response: Response
) -> AuthTokens:
    access_token, refresh_token = await auth_service.register_user(user_in)
    set_refresh_token_cookie(response, refresh_token)
    return AuthTokens(access_token=access_token)


@router.post(
    path="/login",
    response_model=AuthTokens,
    status_code=status.HTTP_200_OK,
)
async def login_user(
    auth_service: AuthServiceDep, user_in: UserLogin, response: Response
) -> AuthTokens:
    access_token, refresh_token = await auth_service.login_user(user_in)
    set_refresh_token_cookie(response, refresh_token)
    return AuthTokens(access_token=access_token)


@router.put(
    path="/me/update",
    response_model=UserCurrent,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    current_user: CurrentUserDep, user_service: UserServiceDep, user_in: UserUpdate
) -> UserCurrent:
    user = await user_service.update_user(current_user, user_in)
    return UserCurrent.model_validate(user)


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
    auth_service: AuthServiceDep,
    refresh_token: str | None = Cookie(default=None),
    response: Response = None,
) -> AuthTokens:
    access_token, refresh_token = await auth_service.refresh_tokens(refresh_token)
    set_refresh_token_cookie(response, refresh_token)
    return AuthTokens(access_token=access_token)
