from typing import List

import structlog

from packages.app.repositories.weather import WeatherRepository
from packages.app.schemas.weather import WeatherStatsResponse, WeatherListResponse
from packages.etl.model import Weather, WeatherStats

logger = structlog.get_logger(__name__)


class WeatherService:
    MAX_RETRIES = 5

    def __init__(
        self,
        weather_repository: WeatherRepository,
    ) -> None:
        self.weather_repository = weather_repository

    async def get_stations(self) -> List[str]:
        stations = await self.weather_repository.get_all_station_ids()

        return stations

    async def get_todays_weather(self, station_id: str) -> List[Weather]:
        weather = await self.weather_repository.get_todays_weather(station_id)

        return weather

    async def get_todays_weather_stats(self) -> List[WeatherStats]:
        stats = await self.weather_repository.get_todays_stats()

        return stats
