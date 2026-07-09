"""
AudioSmith AI — Processing Job Model.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class ProcessingJob(Base, UUIDMixin, TimestampMixin):
    """Processing job model.

    Tracks the lifecycle of an audio enhancement job from
    submission through completion or failure.
    """

    __tablename__ = "processing_jobs"

    # Ownership & references
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False, index=True
    )
    audio_file_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("audio_files.id"), nullable=False
    )
    enhanced_file_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("audio_files.id"), nullable=True
    )

    # Job configuration
    model_name: Mapped[str] = mapped_column(
        String(50), default="deepfilternet", nullable=False
    )

    # Job status tracking
    status: Mapped[str] = mapped_column(
        String(20), default="pending", nullable=False, index=True
    )
    progress_percent: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Result metadata
    waveform_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    spectrogram_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

    # Quality metrics
    pesq_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    stoi_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    si_sdr_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    snr_improvement: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="processing_jobs")
    original_audio: Mapped["AudioFile"] = relationship(
        "AudioFile", foreign_keys=[audio_file_id]
    )
    enhanced_audio: Mapped[Optional["AudioFile"]] = relationship(
        "AudioFile", foreign_keys=[enhanced_file_id]
    )
