# Weather Data ETL Pipeline

This ETL pipeline fetches weather data from the German Weather Service (DWD), processes it, and stores it in a database.

## Requirements

- Python 3.13+
- Redis (for Celery)
- PostgreSQL database
- uv package manager
- Environment variables:
  - `ETL_DATABASE_URL`: Database connection string
  - `REDIS_HOST`: Redis host (default: localhost)
  - `REDIS_PORT`: Redis port (default: 6379)
  - `REDIS_DB`: Redis database number (default: 0)
  - `DEBUG`: Enable debug logging (optional)
  - `CELERY_TIMEZONE`: Timezone for scheduled tasks (default: UTC)

## Installation

1. Install uv if not already installed:
```sh
pip install uv
```

2. Create and activate virtual environment:
```sh
uv venv
.venv\Scripts\activate
```

3. Install dependencies using uv:
```sh
uv pip install .
```

4. Create .env file in project root:
```sh
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
DEBUG=False
CELERY_TIMEZONE=UTC
```

## Running the Pipeline

### Manual Execution
```sh
python -m etl.main
```

### Scheduled Execution

The pipeline runs automatically every day at 00:15 UTC via Celery.

Start the Celery worker:
```sh
celery -A etl.celery worker --loglevel=info
```

Start the Celery beat scheduler:
```sh
celery -A etl.celery beat --loglevel=info
```
