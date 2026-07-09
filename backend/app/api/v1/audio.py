"""
AudioSmith AI — Audio Endpoints.

Handles audio file upload, download, and metadata retrieval.
"""

from __future__ import annotations

from fastapi import APIRouter, UploadFile, File

from app.api.v1.schemas.audio import AudioFileResponse, AudioUploadResponse

router = APIRouter()


@router.post("/upload", response_model=AudioUploadResponse, status_code=201)
async def upload_audio(
    file: UploadFile = File(..., description="Audio file to process"),
) -> AudioUploadResponse:
    """Upload a noisy audio file for processing.

    Validates the file format and size, stores it, and returns a file ID
    that can be used to initiate processing.
    """
    # Future: delegate to AudioService
    raise NotImplementedError("Audio upload not yet implemented.")


@router.get("/{audio_id}", response_model=AudioFileResponse)
async def get_audio_metadata(audio_id: str) -> AudioFileResponse:
    """Get metadata for an uploaded audio file."""
    # Future: delegate to AudioService
    raise NotImplementedError("Audio metadata retrieval not yet implemented.")


@router.get("/{audio_id}/download")
async def download_audio(audio_id: str) -> None:
    """Download an audio file (original or enhanced)."""
    # Future: delegate to AudioService, return StreamingResponse
    raise NotImplementedError("Audio download not yet implemented.")


@router.delete("/{audio_id}", status_code=204)
async def delete_audio(audio_id: str) -> None:
    """Delete an uploaded audio file and its associated data."""
    # Future: delegate to AudioService
    raise NotImplementedError("Audio deletion not yet implemented.")
