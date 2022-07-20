from core.config import config

from celery import Celery

celery_app = Celery(
    title=__name__,
    broker=config.REDIS_DSN,
    backend='redis://localhost',
    include=["app.tasks"]
)
