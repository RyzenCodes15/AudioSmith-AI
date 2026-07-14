"""
AudioSmith AI — Celery Application Configuration.

Configures Celery for distributed audio processing tasks.
"""

from __future__ import annotations

from celery import Celery
from celery.signals import worker_process_init

from app.config import get_settings
from ml.models.base import BaseSpeechEnhancer

# Global cache for loaded models in this worker process
_loaded_models: dict[str, BaseSpeechEnhancer] = {}

def get_loaded_model(name: str) -> BaseSpeechEnhancer:
    """Get a pre-loaded model instance."""
    if name not in _loaded_models:
        raise RuntimeError(f"Model {name} is not loaded.")
    return _loaded_models[name]

@worker_process_init.connect
def init_worker(**kwargs) -> None:
    """Initialize ML models when a worker process starts."""
    from ml.models.registry import get_registry
    from ml.models.deepfilternet import DeepFilterNetAdapter
    import logging
    
    logger = logging.getLogger(__name__)
    logger.info("Initializing ML models in Celery worker process...")
    
    registry = get_registry()
    registry.register("deepfilternet", DeepFilterNetAdapter)
    
    settings = get_settings()
    model_name = settings.ml_model_name
    
    logger.info(f"Loading default model: {model_name}")
    model = registry.create(model_name)
    model.to_device(settings.ml_device)
    
    checkpoint = settings.ml_model_checkpoint_path
    model.load(checkpoint if checkpoint else None)
    
    _loaded_models[model_name] = model
    logger.info(f"Model {model_name} loaded and ready for inference.")


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
