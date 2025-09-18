# backend/celery_app.py
from celery import Celery
import os

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

celery = Celery("market_tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
celery.conf.beat_schedule = {
    # run every 15 minutes
    "fetch-market-every-15m": {
        "task": "app.tasks.fetch_all_sources",
        "schedule": 15 * 60
    }
}
celery.conf.timezone = "UTC"
