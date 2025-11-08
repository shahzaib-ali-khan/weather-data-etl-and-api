from typing import Annotated, Dict, List

from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends

from packages.app.api.dependencies.weather import get_weather_service
from packages.app.api.v1.filters.weather import WeatherFilter
from packages.app.schemas.weather import (WeatherListResponse, WeatherResponse,
                                          WeatherStatsListResponse,
                                          WeatherStatsResponse)
from packages.app.services.weather import WeatherService

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("/stations", response_model=Dict[str, List[str]], summary="Get station list")
async def list_stations(
    weather_service: Annotated[WeatherService, Depends(get_weather_service)],
) -> Dict[str, List[str]]:
    stations_list = await weather_service.get_stations()
    return {"result": stations_list}


@router.get("/today", response_model=WeatherListResponse, summary="Get today's weather")
async def today(
    station_id: str,
    weather_service: Annotated[WeatherService, Depends(get_weather_service)],
    weather_filter: WeatherFilter = FilterDepends(WeatherFilter),
) -> WeatherListResponse:
    weather_data_list = await weather_service.get_todays_weather(station_id, weather_filter)

    weather_data = [
        WeatherResponse(
            station_id=weather.station_id,
            date=weather.date,
            time_utc=weather.time_utc,
            temperature=weather.temperature,
            pressure=weather.pressure,
            humidity=weather.humidity,
            wind_speed=weather.wind_speed,
            wind_direction=weather.wind_direction,
        )
        for weather in weather_data_list
    ]

    return WeatherListResponse(result=weather_data)


@router.get("/today/stats", response_model=WeatherStatsListResponse, summary="Get today's weather stats per station")
async def today_stats(
    weather_service: Annotated[WeatherService, Depends(get_weather_service)],
) -> WeatherStatsListResponse:
    stats_list = await weather_service.get_todays_weather_stats()
    return WeatherStatsListResponse(
        result=[
            WeatherStatsResponse(
                station_id=stat.station_id, date=stat.date, average=stat.average, min=stat.min, max=stat.max
            )
            for stat in stats_list
        ]
    )
