# Weather Data ETL and API

A comprehensive data pipeline project that extracts weather data for Germany, processes it through an ETL pipeline, and exposes it via a FastAPI REST API. This project demonstrates modern Python development practices using UV's workspace feature for monorepo management.

## 🏗️ Project Architecture

This project is structured as a monorepo with two distinct workspaces managed by UV:

```
weather-data-etl-and-api/
├── packages/
│   ├── etl/              # ETL pipeline workspace
│   │   ├── src/
│   │   ├── pyproject.toml
│   │   └── README.md
│   └── app/              # FastAPI application workspace
│       ├── src/
│       └── pyproject.toml
├── pyproject.toml        # Root workspace configuration
└── README.md            # This file
```

### Workspace Overview

#### 1. **ETL Workspace** (`packages/etl/`)
The ETL pipeline is responsible for:
- **Extracting** weather data from external sources
- **Transforming** raw data into a structured format
- **Loading** processed data into a database/storage system

For detailed information about the ETL pipeline, see the [ETL README](packages/etl/README.md).

#### 2. **App Workspace** (`packages/app/`)
The FastAPI application provides:
- RESTful API endpoints to query weather data
- Data validation and serialization
- API documentation (Swagger/OpenAPI)
- Integration with the ETL pipeline's output

## 🚀 Getting Started

### Prerequisites

- Python 3.13 or higher
- [UV](https://github.com/astral-sh/uv) package manager

### Installation

1. **Install UV** (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Clone the repository**:
```bash
git clone https://github.com/shahzaib-ali-khan/weather-data-etl-and-api.git
cd weather-data-etl-and-api
```

3. **Install dependencies** for all workspaces:
```bash
uv sync --all-packages
```

This command will install dependencies for both the ETL and App workspaces defined in the root `pyproject.toml`.

## 📊 Running the ETL Pipeline

Refer to the [ETL README](packages/etl/README.md).

## 🌐 Running the FastAPI Application

After running the ETL pipeline at least once to populate data:

Run (from root directory)

1**Start the FastAPI server**:

```bash
uv run uvicorn packages.app.main:app --host 0.0.0.0 --port 8000 --reload
```

2**Access the API**:
   - API Base URL: `http://localhost:8000/api/v1`
   - Interactive API Docs (Swagger): `http://localhost:8000/api/v1/docs`
   - Alternative API Docs (ReDoc): `http://localhost:8000/api/v1/redoc`

## 📖 API Endpoints

Once the FastAPI application is running, you can interact with the following endpoints (examples):

- `GET /weather/stations` - Retrieve all the weather stations
- `GET /weather/today` - Retrieve today's weather data with optional filters
- `GET /weather/today/stats` - Get statistical summaries for todays weather

*Notes:* 

1. Visit the Swagger documentation at `http://localhost:8000/api/v1/docs` for complete API documentation.
2. In `GET /weather/stations` `station_id` is a required query param

## 🔎 Filters

`GET /weather/stations` supports below filter:

1. time_utc__gte
2. time_utc__lte
3. date__gte
4. date__lte

All of the above are in UTC timezone

## 🔐 Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Database Configuration
APP_DATABASE_URL=postgresql://user:password@localhost:5432/weather_db
```

## 🧪 Testing

The project includes comprehensive tests for both workspaces:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=packages --cov-report=html
```
