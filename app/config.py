"""Application configuration module."""
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Centralized configuration loaded from environment variables."""

    openai_api_key: str | None = None
    csv_catalog_path: str | None = None
    value_proposition_path: str | None = None
    openai_model: str = "gpt-4o-mini"
    redis_url: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance to avoid re-parsing environment."""
    return Settings()
