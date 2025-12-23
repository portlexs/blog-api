from fastapi import HTTPException, status


class SubscriptionAlreadyExistsError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Subscription already exists",
        )


class SubscriptionAuthorNotFoundError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription author not found",
        )


class SelfSubscriptionError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot subscribe to yourself",
        )
