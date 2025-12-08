from fastapi import status, APIRouter

from ..schemas.subscription_schemas import (
    SubscriptionCreate,
    SubscriptionUpdate,
    SubscriptionPublic,
)
from ..schemas.user_schemas import UserPublic
from ..services.dependencies import CurrentUserDep, SubscriptionServiceDep


router = APIRouter(prefix="/users", tags=["subscriptions"])


@router.put(
    path="/me/subscription-key",
    status_code=status.HTTP_200_OK,
)
async def add_subscription_key_to_user(
    current_user: CurrentUserDep,
    subscription_service: SubscriptionServiceDep,
    subscription_in: SubscriptionCreate,
) -> UserPublic:
    user = await subscription_service.add_subscription_key_to_user(
        subscription_in, current_user
    )
    return UserPublic.model_validate(user)


@router.post(
    path="/me/subscribe",
    status_code=status.HTTP_201_CREATED,
)
async def subscribe_current_user(
    current_user: CurrentUserDep,
    subscription_service: SubscriptionServiceDep,
    subscription_in: SubscriptionUpdate,
) -> SubscriptionPublic:
    subscription = await subscription_service.subscribe_user(
        subscription_in, current_user.id
    )
    return SubscriptionPublic.model_validate(subscription)
