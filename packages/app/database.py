from collections.abc import AsyncGenerator
from typing import Optional

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from packages.app.config import settings


class DatabaseManager:
    """Manages database connections and sessions (Singleton pattern)."""

    _instance: Optional["DatabaseManager"] = None

    def __new__(cls) -> "DatabaseManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "engine"):
            self.engine = create_async_engine(
                settings.APP_DATABASE_URL,
                echo=settings.DEBUG,
                future=True,
                connect_args={"check_same_thread": False} if "sqlite" in settings.APP_DATABASE_URL else {},
            )

            self.async_session_maker = async_sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )

    async def close(self) -> None:
        """Close database connection."""
        await self.engine.dispose()


db_manager = DatabaseManager()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async database sessions."""
    async with db_manager.async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
