"""
AudioSmith AI — Base Repository.

Generic CRUD repository providing common database operations.
All specific repositories inherit from this base.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    """Generic async CRUD repository.

    Provides standard create, read, update, delete operations
    for any SQLAlchemy model.
    """

    def __init__(self, model: type[ModelT], session: AsyncSession) -> None:
        self._model = model
        self._session = session

    async def create(self, **kwargs: object) -> ModelT:
        """Create a new record."""
        instance = self._model(**kwargs)
        self._session.add(instance)
        await self._session.flush()
        await self._session.refresh(instance)
        return instance

    async def add(self, instance: ModelT) -> ModelT:
        """Add and persist a model instance created outside the repository."""
        self._session.add(instance)
        await self._session.flush()
        await self._session.refresh(instance)
        return instance

    async def get_by_id(self, id: str) -> ModelT | None:
        """Get a record by its primary key."""
        return await self._session.get(self._model, id)

    async def get_all(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[ModelT]:
        """Get all records with pagination."""
        stmt = select(self._model).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def update(self, instance: ModelT, **kwargs: object) -> ModelT:
        """Update an existing record."""
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await self._session.flush()
        await self._session.refresh(instance)
        return instance

    async def delete(self, instance: ModelT) -> None:
        """Delete a record."""
        await self._session.delete(instance)
        await self._session.flush()
