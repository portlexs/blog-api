from celery import Celery

from ..config import settings

celery_app = Celery("blog_service", broker=settings.celery.broker_url)
celery_app.conf.task_routes = {
    "send_post_notification": "notifications",
}
