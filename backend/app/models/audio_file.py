"""
AudioSmith AI — Audio File Model.
"""

from __future__ import annotations

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class AudioFile(Base, UUIDMixin, TimestampMixin):
    """Audio file metadata model.

    Stores metadata about uploaded and enhanced audio files.
    Actual file bytes are stored via the StorageBackend abstraction.
    """

    __tablename__ = "audio_files"

    # Ownership
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False, index=True
    )

    # File metadata
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(512), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    format: Mapped[str] = mapped_column(String(10), nullable=False)

    # Audio metadata
    duration_seconds: Mapped[float] = mapped_column(Float, nullable=False)
    sample_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    channels: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # File type: "original" | "enhanced"
    file_type: Mapped[str] = mapped_column(
        String(20), default="original", nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="audio_files")
