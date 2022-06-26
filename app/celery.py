from celery import Celery
from core.config import config

celery = Celery(title=__name__, broker=config.REDIS_DSN)
