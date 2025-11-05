from datetime import datetime

import structlog

from .pipeline import run_pipeline

logger = structlog.get_logger()


def main():
    logger.info(f"Pipeline started at {datetime.now()}")
    run_pipeline()
    logger.info(f"Pipeline finished at {datetime.now()}")


if __name__ == "__main__":
    main()
