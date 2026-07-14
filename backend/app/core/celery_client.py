"""
AudioSmith AI — Celery Client.

Lightweight Celery client for the FastAPI backend to send tasks to the worker,
without importing worker dependencies (like ML models).
"""

from celery import Celery
from app.config import get_settings

settings = get_settings()

celery_client = Celery(
    "audiosmith",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_client.conf.update(
    task_default_queue="audio",
    task_default_exchange="audio",
    task_default_routing_key="audio",
)
