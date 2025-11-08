from datetime import date
from sqlalchemy import select, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from packages.etl.model import Weather, WeatherStats


class WeatherRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_station_ids(self) -> list[str]:
        stmt = select(distinct(Weather.station_id)).order_by(Weather.station_id)
        result = await self.session.execute(stmt)
        return [row[0] for row in result.all()]

    async def get_todays_weather(self, station_id: str) -> list[Weather]:
        today = date.today()
        stmt = (
            select(Weather)
            .where(Weather.date == today, Weather.station_id == station_id)
            .order_by(Weather.time_utc)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_todays_stats(self) -> list[WeatherStats]:
        today = date.today()
        stmt = (
            select(WeatherStats)
            .where(WeatherStats.date== today)
            .order_by(WeatherStats.station_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()