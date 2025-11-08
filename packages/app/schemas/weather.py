from datetime import date, time
from typing import Optional, Union

from pydantic import BaseModel, field_validator


class WeatherResponse(BaseModel):
    station_id: Optional[str] = None
    date: date
    time_utc: time
    temperature: Optional[float] = None
    pressure: Optional[float] = None
    humidity: Optional[int] = None
    wind_speed: Optional[float] = None
    wind_direction: Optional[int] = None

    @field_validator("date", mode="before")
    @classmethod
    def validate_date(cls, v: Union[date, None]) -> Union[date, None]:
        if v in (None, "", "---"):
            return None
        return v

    @field_validator("temperature", "pressure", "humidity", "wind_speed", "wind_direction", mode="before")
    @classmethod
    def validate_measurement(cls, v: Union[int, float, None]) -> Union[int, float, None]:
        if v in ("---", "", None):
            return None
        return v

    class Config:
        from_attributes = True


class WeatherListResponse(BaseModel):
    result: list[WeatherResponse]


class WeatherStatsResponse(BaseModel):
    station_id: str
    date: date
    average: float
    min: float
    max: float

    class Config:
        from_attributes = True


class WeatherStatsListResponse(BaseModel):
    result: list[WeatherStatsResponse]
