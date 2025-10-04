from datetime import datetime, timezone

from fastapi import Response

from ..enums.token_type import TokenType


def set_refresh_token_cookie(response: Response, refresh_token: str) -> None:
    expires_time = datetime.now(timezone.utc) + TokenType.REFRESH.value

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        expires=expires_time,
        httponly=True,
        secure=True,
        samesite="strict",
    )
