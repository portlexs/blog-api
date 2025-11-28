from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    def __init__(self, message: str) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials. {message}",
            headers={"WWW-Authenticate": "Bearer"},
        )
