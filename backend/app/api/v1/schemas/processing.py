"""
AudioSmith AI — Processing Schemas.

Pydantic models for processing job request/response validation.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class JobStatus(StrEnum):
    """Processing job status."""

    PENDING = "pending"
    PREPROCESSING = "preprocessing"
    PROCESSING = "processing"
    POSTPROCESSING = "postprocessing"
    COMPLETED = "completed"
    FAILED = "failed"


class ProcessingSubmitRequest(BaseModel):
    """Schema for submitting an audio file for processing."""

    audio_file_id: str = Field(description="ID of the uploaded audio file")
    model_name: str = Field(
        default="deepfilternet",
        description="Name of the ML model to use for enhancement",
    )


class ProcessingJobResponse(BaseModel):
    """Schema for processing job status."""

    id: str
    audio_file_id: str
    model_name: str
    status: JobStatus
    progress_percent: int = Field(default=0, ge=0, le=100)
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None


class ProcessingMetrics(BaseModel):
    """Audio quality metrics for the processing result."""

    pesq: float | None = Field(default=None, description="PESQ score")
    stoi: float | None = Field(default=None, description="STOI score")
    si_sdr: float | None = Field(default=None, description="SI-SDR in dB")
    snr_improvement: float | None = Field(
        default=None, description="SNR improvement in dB"
    )


class ProcessingResultResponse(BaseModel):
    """Schema for processing result with download URLs and visualizations."""

    job_id: str
    original_audio_url: str
    enhanced_audio_url: str
    waveform_comparison_url: str
    spectrogram_comparison_url: str
    metrics: ProcessingMetrics | None = None
