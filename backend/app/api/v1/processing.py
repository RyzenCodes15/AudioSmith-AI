"""
AudioSmith AI — Processing Endpoints.

Handles audio processing job submission, status tracking, and result retrieval.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.schemas.processing import (
    ProcessingJobResponse,
    ProcessingResultResponse,
    ProcessingSubmitRequest,
)

router = APIRouter()


@router.post("/submit", response_model=ProcessingJobResponse, status_code=202)
async def submit_processing_job(
    payload: ProcessingSubmitRequest,
) -> ProcessingJobResponse:
    """Submit an audio file for AI denoising.

    Creates a processing job in the queue and returns a job ID
    for status tracking.
    """
    # Future: delegate to ProcessingService → Celery task
    raise NotImplementedError("Processing submission not yet implemented.")


@router.get("/{job_id}/status", response_model=ProcessingJobResponse)
async def get_job_status(job_id: str) -> ProcessingJobResponse:
    """Get the current status of a processing job."""
    # Future: delegate to ProcessingService
    raise NotImplementedError("Job status retrieval not yet implemented.")


@router.get("/{job_id}/result", response_model=ProcessingResultResponse)
async def get_processing_result(job_id: str) -> ProcessingResultResponse:
    """Get the result of a completed processing job.

    Returns URLs for enhanced audio, waveform comparison,
    and spectrogram comparison.
    """
    # Future: delegate to ProcessingService
    raise NotImplementedError("Result retrieval not yet implemented.")


@router.get("/history", response_model=list[ProcessingJobResponse])
async def get_processing_history() -> list[ProcessingJobResponse]:
    """Get the processing history for the current user."""
    # Future: delegate to ProcessingService
    raise NotImplementedError("Processing history not yet implemented.")
