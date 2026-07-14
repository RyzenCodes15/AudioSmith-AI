"""
AudioSmith AI — Audio Schemas.

Pydantic models for audio file request/response validation.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class AudioUploadResponse(BaseModel):
    """Schema for audio upload response."""

    id: str
    filename: str
    file_size_bytes: int
    duration_seconds: float
    sample_rate: int
    channels: int
    format: str
    uploaded_at: datetime


class AudioFileResponse(BaseModel):
    """Schema for audio file metadata."""

    id: str
    filename: str
    file_size_bytes: int
    duration_seconds: float
    sample_rate: int
    channels: int
    format: str
    uploaded_at: datetime
    status: str = Field(
        description="Current status: uploaded | processing | completed | failed"
    )
    enhanced_file_id: str | None = Field(
        default=None,
        description="ID of the enhanced audio file, if processing is complete",
    )
