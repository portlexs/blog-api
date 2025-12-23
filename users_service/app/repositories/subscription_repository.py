import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.subscription_model import Subscription


class SubscriptionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def subscribe_user(self, subscription: Subscription) -> Subscription:
        self.session.add(subscription)
        await self.session.commit()
        await self.session.refresh(subscription)

        return subscription

    async def get_subscription(
        self, subscriber_id: uuid.UUID, author_id: uuid.UUID
    ) -> Subscription | None:
        query = select(Subscription).where(
            Subscription.subscriber_id == subscriber_id,
            Subscription.author_id == author_id,
        )
        result = await self.session.execute(query)
        return result.scalars().first()
