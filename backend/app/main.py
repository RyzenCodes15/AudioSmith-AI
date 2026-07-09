"""
AudioSmith AI — FastAPI Application Factory.

Creates and configures the FastAPI application instance.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_v1_router
from app.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan — startup and shutdown hooks."""
    settings = get_settings()

    # ── Startup ──────────────────────────────────────────────────────
    # Future: initialize database connection pool
    # Future: warm up ML model
    # Future: connect to Redis

    yield

    # ── Shutdown ─────────────────────────────────────────────────────
    # Future: close database connections
    # Future: cleanup resources


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AI-powered speech enhancement — remove background noise from human speech.",
        docs_url="/api/docs" if not settings.is_production else None,
        redoc_url="/api/redoc" if not settings.is_production else None,
        openapi_url="/api/openapi.json" if not settings.is_production else None,
        lifespan=lifespan,
    )

    # ── Middleware ────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Routers ──────────────────────────────────────────────────────
    app.include_router(api_v1_router, prefix="/api/v1")

    return app


# Application instance for uvicorn
app = create_app()
