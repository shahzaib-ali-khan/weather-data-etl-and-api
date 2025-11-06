import os
from sqlalchemy import Engine, create_engine

from .model import Base


def create_db_engine() -> Engine:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise Exception("DATABASE_URL is not set")

    return create_engine(
        database_url,
        echo=bool(os.getenv("DEBUG")),
        future=True,
    )


def init_db() -> None:
    db_engine = create_db_engine()
    Base.metadata.create_all(db_engine)
