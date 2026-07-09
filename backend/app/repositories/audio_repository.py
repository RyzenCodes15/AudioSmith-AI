"""
AudioSmith AI — Audio Repository.

Data access layer for audio file database operations.
"""

from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audio_file import AudioFile
from app.repositories.base import BaseRepository


class AudioRepository(BaseRepository[AudioFile]):
    """Repository for AudioFile model operations."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(AudioFile, session)

    async def get_by_user(
        self,
        user_id: str,
        *,
        skip: int = 0,
        limit: int = 50,
    ) -> Sequence[AudioFile]:
        """Get all audio files for a specific user."""
        stmt = (
            select(AudioFile)
            .where(AudioFile.user_id == user_id)
            .order_by(AudioFile.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()
