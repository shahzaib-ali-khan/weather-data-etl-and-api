import uuid

from sqlalchemy import Column, Date, DateTime, Float, Integer, String, Time
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def generate_uuid() -> str:
    return str(uuid.uuid4())


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(String, nullable=False)
    source_file = Column(String)
    date = Column(Date, nullable=False)
    time_utc = Column(Time, nullable=False)
    datetime = Column(DateTime, nullable=False)
    temperature = Column(String, nullable=True)


class TemperatureStats(Base):
    __tablename__ = "temperature_stats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    average = Column(Float, nullable=False)
    min = Column(Float, nullable=False)
    max = Column(Float, nullable=False)
