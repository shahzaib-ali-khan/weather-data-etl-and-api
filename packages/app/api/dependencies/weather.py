from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from packages.app.database import get_session
from packages.app.repositories.weather import WeatherRepository
from packages.app.services.weather import WeatherService


async def get_weather_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> WeatherRepository:
    return WeatherRepository(session)


async def get_weather_service(
    weather_repository: Annotated[WeatherRepository, Depends(get_weather_repository)],
) -> WeatherService:
    return WeatherService(weather_repository)
