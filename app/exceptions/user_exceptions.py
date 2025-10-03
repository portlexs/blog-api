from fastapi import HTTPException, status


class UserAlreadyExistsError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User already exists",
        )


class UserNotFoundError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found",
        )


class InvalidLoginOrPasswordError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid login or password",
        )
