from fastapi import HTTPException, status


class ArticleNotFoundError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
