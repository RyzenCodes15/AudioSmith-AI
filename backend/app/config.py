"""
AudioSmith AI — Application Configuration.

Environment-driven configuration using Pydantic Settings.
All settings are loaded from environment variables or .env file.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── General ──────────────────────────────────────────────────────────
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = True
    log_level: str = "INFO"
    app_name: str = "AudioSmith AI"
    app_version: str = "0.1.0"

    # ── Backend Server ───────────────────────────────────────────────────
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    backend_cors_origins: list[str] = ["http://localhost:3000"]

    # ── Database ─────────────────────────────────────────────────────────
    database_url: str = (
        "postgresql+asyncpg://audiosmith:audiosmith_dev_password"
        "@localhost:5432/audiosmith"
    )

    # ── Redis ────────────────────────────────────────────────────────────
    redis_url: str = "redis://localhost:6379/0"

    # ── Authentication (JWT) ─────────────────────────────────────────────
    jwt_secret_key: str = "change-this-to-a-random-secret-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # ── Storage ──────────────────────────────────────────────────────────
    storage_backend: Literal["local", "s3"] = "local"
    storage_local_path: str = "./storage"

    # ── ML / Inference ───────────────────────────────────────────────────
    ml_model_name: str = "deepfilternet"
    ml_model_checkpoint_path: str = ""
    ml_device: str = "cpu"
    ml_max_audio_duration_seconds: int = 300
    ml_sample_rate: int = 48000

    # ── Celery ───────────────────────────────────────────────────────────
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached application settings singleton."""
    return Settings()
