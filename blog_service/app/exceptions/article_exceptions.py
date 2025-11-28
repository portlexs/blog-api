from fastapi import HTTPException, status


class ArticleNotFoundError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )


class ArticleAlreadyExistsError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Article already exists",
        )
