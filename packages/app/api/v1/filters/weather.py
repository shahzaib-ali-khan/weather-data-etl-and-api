from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter

from packages.etl.model import Weather


class WeatherFilter(Filter):
    time_utc__gte: Optional[str] = None
    time_utc__lte: Optional[str] = None

    date__gte: Optional[str] = None
    date__lte: Optional[str] = None

    class Constants(Filter.Constants):
        model = Weather
        fields = ["time_utc", "date"]
