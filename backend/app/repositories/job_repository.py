"""
AudioSmith AI — Job Repository.

Data access layer for processing job database operations.
"""

from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.processing_job import ProcessingJob
from app.repositories.base import BaseRepository


class JobRepository(BaseRepository[ProcessingJob]):
    """Repository for ProcessingJob model operations."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ProcessingJob, session)

    async def get_by_user(
        self,
        user_id: str,
        *,
        skip: int = 0,
        limit: int = 50,
    ) -> Sequence[ProcessingJob]:
        """Get all processing jobs for a specific user."""
        stmt = (
            select(ProcessingJob)
            .where(ProcessingJob.user_id == user_id)
            .order_by(ProcessingJob.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_pending_jobs(self, *, limit: int = 10) -> Sequence[ProcessingJob]:
        """Get pending jobs for worker processing."""
        stmt = (
            select(ProcessingJob)
            .where(ProcessingJob.status == "pending")
            .order_by(ProcessingJob.created_at.asc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()
