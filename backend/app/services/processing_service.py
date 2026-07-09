"""
AudioSmith AI — Processing Service.

Business logic for audio processing job management.
"""

from __future__ import annotations

from app.core.exceptions import NotFoundError
from app.repositories.job_repository import JobRepository


class ProcessingService:
    """Handles processing job business logic.

    Coordinates job creation, status tracking, and result retrieval.
    Delegates actual processing to Celery workers.
    """

    def __init__(self, job_repo: JobRepository) -> None:
        self._job_repo = job_repo

    async def submit_job(
        self,
        user_id: str,
        audio_file_id: str,
        model_name: str = "deepfilternet",
    ) -> dict:
        """Submit a new processing job.

        Creates a job record and enqueues it for Celery worker processing.

        Args:
            user_id: ID of the submitting user.
            audio_file_id: ID of the audio file to process.
            model_name: Name of the ML model to use.

        Returns:
            Created job data.
        """
        # Future: create job record, dispatch Celery task
        raise NotImplementedError("Job submission not yet implemented.")

    async def get_status(self, job_id: str, user_id: str) -> dict:
        """Get the current status of a processing job.

        Args:
            job_id: ID of the processing job.
            user_id: ID of the requesting user.

        Returns:
            Job status data.

        Raises:
            NotFoundError: If the job doesn't exist.
        """
        job = await self._job_repo.get_by_id(job_id)
        if not job or job.user_id != user_id:
            raise NotFoundError("Processing job", job_id)
        # Future: convert to response dict
        raise NotImplementedError("Job status retrieval not yet implemented.")

    async def get_result(self, job_id: str, user_id: str) -> dict:
        """Get the result of a completed processing job.

        Args:
            job_id: ID of the processing job.
            user_id: ID of the requesting user.

        Returns:
            Processing result with URLs and metrics.

        Raises:
            NotFoundError: If the job doesn't exist.
        """
        job = await self._job_repo.get_by_id(job_id)
        if not job or job.user_id != user_id:
            raise NotFoundError("Processing job", job_id)
        # Future: build result response with visualization URLs
        raise NotImplementedError("Result retrieval not yet implemented.")
