import structlog

from .celery import app
from .main import main

logger = structlog.get_logger()


@app.task
def run_pipeline_task():
    logger.info("Celery task triggered")
    main()
