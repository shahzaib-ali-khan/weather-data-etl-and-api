from sqlalchemy import Column, Date, DateTime, Float, Integer, String, Time
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(String, nullable=False)
    source_file = Column(String)
    date = Column(Date, nullable=False)
    time_utc = Column(Time, nullable=False)
    datetime = Column(DateTime, nullable=False)
    temperature = Column(String, nullable=True)
    pressure = Column(Float)
    humidity = Column(Integer, nullable=True)
    wind_speed = Column(Integer, nullable=True)
    wind_direction = Column(Integer, nullable=True)


class WeatherStats(Base):
    __tablename__ = "weather_stats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    average = Column(Float, nullable=False)
    min = Column(Float, nullable=False)
    max = Column(Float, nullable=False)
