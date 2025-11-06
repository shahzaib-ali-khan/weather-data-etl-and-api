from celery import Celery
from celery.schedules import crontab

app = Celery("celery_app", broker="redis://localhost:6379/0")
app.conf.update(
    result_backend="redis://localhost:6379/0",
    beat_schedule={
        "run-etl-pipeline": {
            "task": "tasks.run_pipeline_task",
            "schedule": crontab(hour="00", minute="15"),
        },
    },
    include=["tasks"],
)
