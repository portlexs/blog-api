import uuid

from ..exceptions.subscription_exception import (
    SubscriptionAlreadyExistsError,
    SubscriptionAuthorNotFoundError,
    SelfSubscriptionError,
)
from ..models.subscription_model import Subscription
from ..models.user_model import User
from ..repositories.user_repository import UserRepository
from ..repositories.subscription_repository import SubscriptionRepository
from ..schemas.subscription_schemas import SubscriptionCreate, SubscriptionUpdate


class SubscriptionService:
    def __init__(
        self,
        user_repository: UserRepository,
        subscribtion_repository: SubscriptionRepository,
    ) -> None:
        self.user_repository = user_repository
        self.subscription_repository = subscribtion_repository

    async def add_subscription_key_to_user(
        self, subscription_in: SubscriptionCreate, current_user: User
    ) -> User:
        user = await self.user_repository.update_user(current_user, subscription_in)
        return user

    async def subscribe_user(
        self, subscription_in: SubscriptionUpdate, current_user_id: uuid.UUID
    ) -> Subscription:
        if current_user_id == subscription_in.author_id:
            raise SelfSubscriptionError()

        existing_author = await self.user_repository.get_user_by_id(
            subscription_in.author_id
        )
        if not existing_author:
            raise SubscriptionAuthorNotFoundError()

        existing_subscription = await self.subscription_repository.get_subscription(
            current_user_id, subscription_in.author_id
        )
        if existing_subscription:
            raise SubscriptionAlreadyExistsError()

        subscription = Subscription(
            subscriber_id=current_user_id, author_id=subscription_in.author_id
        )
        new_subscription = await self.subscription_repository.subscribe_user(
            subscription
        )
        return new_subscription
