from datetime import date
from typing import Optional

from sqlalchemy import select, distinct, and_
from sqlalchemy.ext.asyncio import AsyncSession

from packages.app.api.v1.filters.weather import WeatherFilter
from packages.etl.model import Weather, WeatherStats


class WeatherRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_station_ids(self) -> list[str]:
        stmt = select(distinct(Weather.station_id)).order_by(Weather.station_id)
        result = await self.session.execute(stmt)
        return [row[0] for row in result.all()]

    async def get_todays_weather(self, station_id: str, weather_filter: Optional[WeatherFilter] = None) -> list[Weather]:
        today = date.today()
        statement = (
            select(Weather)
            .where(
                and_(
                    Weather.date == today,
                    Weather.station_id == station_id
                )
            )
            .order_by(Weather.time_utc)
        )

        if weather_filter:
            statement = weather_filter.filter(statement)

        result = await self.session.execute(statement)

        return list(result.scalars().all())

    async def get_todays_stats(self) -> list[WeatherStats]:
        today = date.today()

        statement = select(WeatherStats).where(
            and_(WeatherStats.date == today)
        ).order_by(WeatherStats.station_id)

        result = await self.session.execute(statement)

        return list(result.scalars().all())
