import asyncio
import logging

import httpx
from celery import Celery
from sqlalchemy import select

from .config import settings
from .database import AsyncSessionLocal
from .models import User, Subscription


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

celery_app = Celery("notification_worker", broker=settings.celery_broker_url)
celery_app.conf.task_routes = {"send_post_notification": "notifications"}


async def _process_notification(author_id: str, article_id: str, post_title: str):
    logger.info(f"Processing notification for post {article_id} by author {author_id}")

    async with AsyncSessionLocal() as session:
        try:
            query = (
                select(User)
                .join(Subscription, Subscription.subscriber_id == User.id)
                .where(Subscription.author_id == author_id)
                .where(User.is_active == True)
                .where(User.subscription_key.isnot(None))
            )

            result = await session.execute(query)
            subscribers = result.scalars().all()

            if not subscribers:
                logger.info("No subscribers with keys found.")
                return

            async with httpx.AsyncClient(timeout=5.0) as client:
                for sub in subscribers:
                    key = sub.subscription_key

                    payload = {
                        "message": f"Пользователь {author_id} выпустил новый пост: {post_title[:10]}..."
                    }
                    headers = {
                        "Authorization": f"Bearer {key}",
                        "Content-Type": "application/json",
                    }

                    try:

                        response = await client.post(
                            settings.push_service_url, json=payload, headers=headers
                        )
                        response.raise_for_status()
                        logger.info(f"Sent push to user {sub.id}")
                    except httpx.RequestError as e:
                        logger.error(f"Failed to push to {sub.id}: {e}")

        except Exception as e:
            logger.error(f"Task failed: {e}")


@celery_app.task(name="send_post_notification", bind=True, max_retries=3)
def send_post_notification(self, author_id: str, article_id: str, post_title: str):
    logger.info(f"Processing notification for post {article_id} by author {author_id}")

    try:
        asyncio.run(_process_notification(author_id, article_id, post_title))
    except Exception as e:
        logger.error(f"Task failed: {e}")
        self.retry(exc=e, countdown=10 * (self.request.retries + 1))
