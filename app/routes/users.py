from fastapi import APIRouter, Depends

from core.auth_dependencies import CurrentUser
from services.users import UserService, get_user_service
from schemas.users import (
    UserCreateRequest,
    UserInfoResponse,
    UserLoginRequest,
    UserLoginResponse,
    UserUpdateRequest,
)


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
async def get_current_user(current_user: CurrentUser) -> UserInfoResponse:
    """Get current user in blog"""
    return UserInfoResponse.model_validate(current_user)


@router.post("/")
async def register_user(
    user_in: UserCreateRequest, user_service: UserService = Depends(get_user_service)
) -> UserInfoResponse:
    return user_service.register_user(user_in)


@router.post("/login")
async def login_user(
    user_in: UserLoginRequest, user_service: UserService = Depends(get_user_service)
) -> UserLoginResponse:
    """Login user in blog"""
    return user_service.login_user(user_in)


@router.put("/me")
async def update_user(
    user_in: UserUpdateRequest,
    current_user: CurrentUser,
    user_service: UserService = Depends(get_user_service),
) -> UserInfoResponse:
    """Update user in blog by id"""
    return user_service.update_user(current_user, user_in)


@router.post("/refresh")
async def refresh_token(
    refresh_token: str, user_service: UserService = Depends(get_user_service)
) -> UserLoginResponse:
    """Refresh token in blog"""
    return user_service.refresh_user_token(refresh_token)
