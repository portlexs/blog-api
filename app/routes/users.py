from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status

from auth.dependencies import CurrentUser
from services.users import UserService, get_user_service
from schemas.users import (
    UserCreate,
    UserInfoResponse,
    UserLogin,
    UserLoginResponse,
    UserUpdate,
)


router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/me",
    response_model=UserInfoResponse,
    status_code=status.HTTP_200_OK,
)
async def get_current_user(current_user: CurrentUser) -> UserInfoResponse:
    """Get current user in blog"""
    return UserInfoResponse.model_validate(current_user)


@router.post(
    "/",
    response_model=UserInfoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_in: UserCreate, user_service: UserService = Depends(get_user_service)
) -> UserInfoResponse:
    """Register user in blog"""
    user = user_service.register_user(user_in)
    return UserInfoResponse.model_validate(user)


@router.post(
    "/login",
    response_model=UserLoginResponse,
    status_code=status.HTTP_200_OK,
)
async def login_user(
    user_in: UserLogin,
    response: Response,
    user_service: UserService = Depends(get_user_service),
) -> UserLoginResponse:
    """Login user in blog"""
    access_token, refresh_token = user_service.login_user(user_in)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )
    return UserLoginResponse(access_token=access_token)


@router.put(
    "/me",
    response_model=UserInfoResponse,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_in: UserUpdate,
    current_user: CurrentUser,
    user_service: UserService = Depends(get_user_service),
) -> UserInfoResponse:
    """Update user in blog"""
    user = user_service.update_user(current_user, user_in)
    return UserInfoResponse.model_validate(user)


@router.post(
    "/refresh",
    response_model=UserLoginResponse,
    status_code=status.HTTP_200_OK,
)
async def refresh_token(
    response: Response,
    refresh_token: str = Cookie(default=None),
    user_service: UserService = Depends(get_user_service),
) -> UserLoginResponse:
    """Refresh user tokens"""
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token provided")

    access_token, refresh_token = user_service.refresh_user_token(refresh_token)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )
    return UserLoginResponse(access_token=access_token)
