"""
AudioSmith AI — Celery Application Configuration.

Configures Celery for distributed audio processing tasks.
"""

from __future__ import annotations

from celery import Celery

from app.config import get_settings


def create_celery_app() -> Celery:
    """Create and configure the Celery application."""
    settings = get_settings()

    celery_app = Celery(
        "audiosmith",
        broker=settings.celery_broker_url,
        backend=settings.celery_result_backend,
    )

    celery_app.conf.update(
        # Serialization
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],

        # Timezone
        timezone="UTC",
        enable_utc=True,

        # Task settings
        task_track_started=True,
        task_time_limit=600,  # 10 minutes hard limit
        task_soft_time_limit=540,  # 9 minutes soft limit
        task_acks_late=True,
        worker_prefetch_multiplier=1,

        # Result settings
        result_expires=86400,  # 24 hours

        # Task routing
        task_routes={
            "worker.tasks.audio_processing.*": {"queue": "audio"},
        },

        # Auto-discover tasks
        include=["worker.tasks.audio_processing"],
    )

    return celery_app


# Celery app instance
celery_app = create_celery_app()
