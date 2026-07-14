"""
AudioSmith AI — Audio Service.

Business logic for audio file management (upload, retrieval, deletion).
"""

from __future__ import annotations

import io
import uuid
from datetime import datetime
from pathlib import Path

import mutagen

from app.config import Settings
from app.core.exceptions import NotFoundError, ValidationError
from app.models.audio_file import AudioFile
from app.models.processing_job import ProcessingJob
from app.repositories.audio_repository import AudioRepository
from app.repositories.job_repository import JobRepository
from app.services.storage.base import StorageBackend


class AudioService:
    """Handles audio file business logic.

    Coordinates between the AudioRepository (metadata) and
    StorageBackend (file bytes) to manage audio files.
    """

    def __init__(
        self,
        audio_repo: AudioRepository,
        job_repo: JobRepository,
        storage: StorageBackend,
        settings: Settings,
    ) -> None:
        self._audio_repo = audio_repo
        self._job_repo = job_repo
        self._storage = storage
        self._settings = settings

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
            Created audio file metadata matching AudioUploadResponse.
        """
        # Validate file size
        file_size = len(content)
        if file_size == 0:
            raise ValidationError("File is empty.")
        if file_size > self._settings.upload_max_size_bytes:
            raise ValidationError(f"File size exceeds maximum allowed ({self._settings.upload_max_size_bytes} bytes).")

        # Validate extension
        ext = Path(filename).suffix.lower()
        if ext not in self._settings.upload_allowed_extensions:
            raise ValidationError(f"Unsupported file extension. Allowed: {', '.join(self._settings.upload_allowed_extensions)}")

        # Extract audio metadata
        try:
            audio_info = mutagen.File(io.BytesIO(content), easy=True)
            if audio_info is None:
                raise ValidationError("Invalid or corrupted audio file.")
            duration = audio_info.info.length
            sample_rate = getattr(audio_info.info, "sample_rate", 44100)
            channels = getattr(audio_info.info, "channels", 2)
        except Exception as e:
            raise ValidationError(f"Failed to parse audio metadata: {e}")

        # Validate duration
        if duration > self._settings.ml_max_audio_duration_seconds:
            raise ValidationError(f"Audio duration exceeds maximum allowed ({self._settings.ml_max_audio_duration_seconds} seconds).")

        # Generate unique storage path
        file_id = str(uuid.uuid4())
        storage_path = f"users/{user_id}/uploads/{file_id}{ext}"

        # Save via StorageBackend
        await self._storage.save(storage_path, content)

        # Create AudioFile record
        audio_file = AudioFile(
            id=file_id,
            user_id=user_id,
            filename=filename,
            storage_path=storage_path,
            file_size_bytes=file_size,
            format=ext.lstrip("."),
            duration_seconds=duration,
            sample_rate=sample_rate,
            channels=channels,
            file_type="original",
        )
        await self._audio_repo.add(audio_file)

        # Create ProcessingJob record
        job_id = str(uuid.uuid4())
        processing_job = ProcessingJob(
            id=job_id,
            user_id=user_id,
            audio_file_id=file_id,
            model_name=self._settings.ml_model_name,
            status="pending",
        )
        await self._job_repo.add(processing_job)

        return {
            "id": file_id,
            "filename": filename,
            "file_size_bytes": file_size,
            "duration_seconds": duration,
            "sample_rate": sample_rate,
            "channels": channels,
            "format": ext.lstrip("."),
            "uploaded_at": audio_file.created_at or datetime.utcnow(),
        }

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

        # Get related job status
        jobs = await self._job_repo.get_by_user(user_id)
        status = "completed"
        enhanced_file_id = None
        for job in jobs:
            if job.audio_file_id == audio_id:
                status = job.status
                enhanced_file_id = job.enhanced_file_id
                break

        return {
            "id": audio.id,
            "filename": audio.filename,
            "file_size_bytes": audio.file_size_bytes,
            "duration_seconds": audio.duration_seconds,
            "sample_rate": audio.sample_rate,
            "channels": audio.channels,
            "format": audio.format,
            "uploaded_at": audio.created_at,
            "status": status,
            "enhanced_file_id": enhanced_file_id,
        }

    async def get_user_uploads(self, user_id: str) -> list[dict]:
        """Get all audio uploads for a user."""
        audios = await self._audio_repo.get_by_user(user_id)
        jobs = await self._job_repo.get_by_user(user_id)

        job_map = {job.audio_file_id: job for job in jobs}

        results = []
        for audio in audios:
            if audio.file_type != "original":
                continue

            job = job_map.get(audio.id)
            results.append({
                "id": audio.id,
                "filename": audio.filename,
                "file_size_bytes": audio.file_size_bytes,
                "duration_seconds": audio.duration_seconds,
                "sample_rate": audio.sample_rate,
                "channels": audio.channels,
                "format": audio.format,
                "uploaded_at": audio.created_at,
                "status": job.status if job else "completed",
                "enhanced_file_id": job.enhanced_file_id if job else None,
            })

        return results

    async def delete(self, audio_id: str, user_id: str) -> None:
        """Delete an audio file and its storage."""
        audio = await self._audio_repo.get_by_id(audio_id)
        if not audio or audio.user_id != user_id:
            raise NotFoundError("Audio file", audio_id)

        try:
            await self._storage.delete(audio.storage_path)
        except Exception:
            pass # Ignore if already deleted

        await self._audio_repo.delete(audio)
