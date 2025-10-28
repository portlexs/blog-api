from datetime import datetime, timezone

from fastapi.responses import JSONResponse

from ..enums.token_type import TokenType


def create_auth_response(
    access_token: str, refresh_token: str, status_code: int
) -> None:
    response = JSONResponse(
        content={"access_token": access_token}, status_code=status_code
    )

    expires_time = datetime.now(timezone.utc) + TokenType.REFRESH.value
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        expires=expires_time,
        httponly=True,
        secure=True,
        samesite="strict",
    )

    return response
