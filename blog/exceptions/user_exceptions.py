from fastapi import HTTPException, status


class UserAlreadyExists(HTTPException):
    def __init__(self, entity: str, field: str, value: str) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{entity} with {field}={value} already exists",
        )
