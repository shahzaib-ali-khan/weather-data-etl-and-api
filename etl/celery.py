import os

from celery import Celery
from celery.schedules import crontab

# Redis configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_DB = os.getenv("REDIS_DB", "0")
CELERY_TIMEZONE = os.getenv("CELERY_TIMEZONE", "UTC")


REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

app = Celery("weather_etl", broker=REDIS_URL)

app.conf.update(
    result_backend=REDIS_URL,
    timezone=CELERY_TIMEZONE,
    beat_schedule={
        "run-etl-pipeline": {
            "task": "etl.tasks.run_pipeline_task",
            "schedule": crontab(hour="00", minute="15"),
        },
    },
    include=["etl.tasks"],
)
