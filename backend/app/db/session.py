"""
AudioSmith AI — Database Session Factory.

Provides async SQLAlchemy session management.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import get_settings


def create_engine():
    """Create an async SQLAlchemy engine."""
    settings = get_settings()

    return create_async_engine(
        settings.database_url,
        echo=settings.debug,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
    )


def create_session_factory(engine=None) -> async_sessionmaker[AsyncSession]:
    """Create an async session factory.

    Args:
        engine: SQLAlchemy async engine. If None, creates a new one.

    Returns:
        Async session factory.
    """
    if engine is None:
        engine = create_engine()

    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
