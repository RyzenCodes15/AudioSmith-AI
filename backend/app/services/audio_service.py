"""
AudioSmith AI — Audio Service.

Business logic for audio file management (upload, retrieval, deletion).
"""

from __future__ import annotations

from app.core.exceptions import NotFoundError
from app.repositories.audio_repository import AudioRepository
from app.services.storage.base import StorageBackend


class AudioService:
    """Handles audio file business logic.

    Coordinates between the AudioRepository (metadata) and
    StorageBackend (file bytes) to manage audio files.
    """

    def __init__(
        self,
        audio_repo: AudioRepository,
        storage: StorageBackend,
    ) -> None:
        self._audio_repo = audio_repo
        self._storage = storage

    async def upload(
        self,
        user_id: str,
        filename: str,
        content: bytes,
        content_type: str,
    ) -> dict:
        """Upload and store an audio file.

        Args:
            user_id: ID of the uploading user.
            filename: Original filename.
            content: Raw file bytes.
            content_type: MIME type of the file.

        Returns:
            Created audio file metadata.
        """
        # Future: validate format, extract audio metadata (duration, sr, channels)
        # Future: store via StorageBackend
        # Future: create AudioFile record via repository
        raise NotImplementedError("Audio upload not yet implemented.")

    async def get_metadata(self, audio_id: str, user_id: str) -> dict:
        """Get audio file metadata.

        Args:
            audio_id: ID of the audio file.
            user_id: ID of the requesting user (for authorization).

        Returns:
            Audio file metadata dict.

        Raises:
            NotFoundError: If the audio file doesn't exist.
        """
        audio = await self._audio_repo.get_by_id(audio_id)
        if not audio or audio.user_id != user_id:
            raise NotFoundError("Audio file", audio_id)
        # Future: convert to response dict
        raise NotImplementedError("Audio metadata retrieval not yet implemented.")

    async def delete(self, audio_id: str, user_id: str) -> None:
        """Delete an audio file and its storage.

        Args:
            audio_id: ID of the audio file.
            user_id: ID of the requesting user (for authorization).

        Raises:
            NotFoundError: If the audio file doesn't exist.
        """
        audio = await self._audio_repo.get_by_id(audio_id)
        if not audio or audio.user_id != user_id:
            raise NotFoundError("Audio file", audio_id)
        # Future: delete from storage, then from database
        raise NotImplementedError("Audio deletion not yet implemented.")
