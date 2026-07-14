"""
AudioSmith AI — Audio Endpoints.

Handles audio file upload, download, and metadata retrieval.
"""

from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile, Response

from app.api.v1.schemas.audio import AudioFileResponse, AudioUploadResponse
from app.dependencies import AudioServiceDep, CurrentUserDep

router = APIRouter()


@router.post("/upload", response_model=AudioUploadResponse, status_code=201)
async def upload_audio(
    current_user: CurrentUserDep,
    audio_service: AudioServiceDep,
    file: UploadFile = File(..., description="Audio file to process"),
) -> AudioUploadResponse:
    """Upload a noisy audio file for processing.

    Validates the file format and size, stores it, and returns a file ID
    that can be used to initiate processing.
    """
    content = await file.read()
    try:
        result = await audio_service.upload(
            user_id=current_user.id,
            filename=file.filename or "unknown",
            content=content,
            content_type=file.content_type or "application/octet-stream",
        )
        return AudioUploadResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[AudioFileResponse])
async def get_user_uploads(
    current_user: CurrentUserDep,
    audio_service: AudioServiceDep,
) -> list[AudioFileResponse]:
    """Get processing history for the current user."""
    results = await audio_service.get_user_uploads(current_user.id)
    return [AudioFileResponse(**res) for res in results]


@router.get("/{audio_id}", response_model=AudioFileResponse)
async def get_audio_metadata(
    audio_id: str,
    current_user: CurrentUserDep,
    audio_service: AudioServiceDep,
) -> AudioFileResponse:
    """Get metadata for an uploaded audio file."""
    result = await audio_service.get_metadata(audio_id, current_user.id)
    return AudioFileResponse(**result)


@router.get("/{audio_id}/download")
async def download_audio(
    audio_id: str,
    current_user: CurrentUserDep,
    audio_service: AudioServiceDep,
) -> Response:
    """Download an audio file (original or enhanced)."""
    try:
        content, filename = await audio_service.get_audio_content(audio_id, current_user.id)
        # Determine content type based on extension
        ext = filename.split(".")[-1].lower() if "." in filename else "wav"
        media_type = f"audio/{ext}"
        if ext == "mp3":
            media_type = "audio/mpeg"
        
        return Response(
            content=content,
            media_type=media_type,
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{audio_id}", status_code=204)
async def delete_audio(
    audio_id: str,
    current_user: CurrentUserDep,
    audio_service: AudioServiceDep,
) -> None:
    """Delete an uploaded audio file and its associated data."""
    await audio_service.delete(audio_id, current_user.id)

