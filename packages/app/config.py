from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    # Application
    APP_NAME: str = "FastAPI Weather App"
    DEBUG: bool = False

    APP_DATABASE_URL: str = f"sqlite+aiosqlite:///./db.sqlite3"

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]


# Create global settings instance
settings = Settings()
