from datetime import datetime

import structlog

from .database import init_db
from .pipeline import run_pipeline

logger = structlog.get_logger()


def main() -> None:
    logger.info(f"Pipeline started at {datetime.now()}")
    init_db()
    run_pipeline()
    logger.info(f"Pipeline finished at {datetime.now()}")


if __name__ == "__main__":
    main()
