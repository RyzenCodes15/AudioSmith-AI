"""
AudioSmith AI — Audio Processing Tasks.

Celery tasks for audio enhancement processing.
These run in a separate worker process, not in the API server.
"""

from __future__ import annotations

import asyncio
import io
import logging
import uuid
import torch

from worker.celery_app import celery_app, get_loaded_model

logger = logging.getLogger(__name__)

async def _process_audio(job_id: str) -> dict:
    import torchaudio
    from app.db.session import create_session_factory
    from app.repositories.job_repository import JobRepository
    from app.repositories.audio_repository import AudioRepository
    from app.services.storage.local import LocalStorageBackend
    from app.models.audio_file import AudioFile
    from app.config import get_settings

    settings = get_settings()
    session_factory = create_session_factory()
    
    async with session_factory() as session:
        job_repo = JobRepository(session)
        audio_repo = AudioRepository(session)
        storage_service = LocalStorageBackend(base_path=settings.storage_local_path)
        
        job = await job_repo.get_by_id(job_id)
        if not job:
            raise ValueError(f"Job {job_id} not found")
            
        job.status = "processing"
        await session.commit()
        
        original_audio = await audio_repo.get_by_id(job.audio_file_id)
        if not original_audio:
            job.status = "failed"
            job.error_message = f"Original audio {job.audio_file_id} not found"
            await session.commit()
            logger.error(job.error_message)
            raise ValueError(job.error_message)
            
        try:
            # 1. Load audio
            logger.info(f"Worker received job: {job_id}, starting audio load")
            audio_path = await storage_service.get_url(original_audio.storage_path)
            
            import soundfile as sf
            data, sample_rate = sf.read(audio_path)
            
            # Ensure shape is [channels, frames] and type is float32
            if len(data.shape) == 1:
                waveform = torch.from_numpy(data).unsqueeze(0).float()
            else:
                waveform = torch.from_numpy(data).transpose(0, 1).float()
                
            logger.info(f"Audio loaded: {original_audio.filename} ({waveform.shape}, {sample_rate}Hz)")
            
            # 2. Get Model
            model = get_loaded_model(settings.ml_model_name)
            target_sr = model.get_sample_rate()
            logger.info(f"Model loaded: {settings.ml_model_name}")
            
            # 3. Preprocess
            if sample_rate != target_sr:
                import torchaudio
                resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=target_sr)
                waveform = resampler(waveform)
                
            # DeepFilterNet expects mono or stereo. Let's make sure it's correct.
            # Usually we don't need to force mono unless required.
            
            # 4. Enhance
            logger.info("Inference started")
            enhanced = model.enhance(waveform)
            logger.info("Inference completed")
            
            # peak normalize
            max_val = torch.max(torch.abs(enhanced))
            if max_val > 0:
                enhanced = enhanced / max_val * 0.99
            
            # 5. Postprocess: Save to a temporary file first
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=".wav") as tmp_file:
                # Transpose back to [frames, channels] for soundfile
                out_data = enhanced.cpu().squeeze().numpy()
                if len(out_data.shape) == 2:
                    out_data = out_data.transpose(1, 0)
                sf.write(tmp_file.name, out_data, target_sr, format='WAV', subtype='PCM_16')
                
                with open(tmp_file.name, "rb") as f:
                    enhanced_bytes = f.read()
            
            # 6. Store
            new_file_id = str(uuid.uuid4())
            new_filename = f"enhanced_{original_audio.filename}"
            if not new_filename.endswith('.wav'):
                new_filename = new_filename.rsplit('.', 1)[0] + '.wav'
                
            path = await storage_service.save(
                f"enhanced_{new_file_id}.wav",
                enhanced_bytes
            )
            logger.info(f"Output saved: {path}")
            
            # 7. Create DB record for enhanced audio
            enhanced_audio = AudioFile(id=new_file_id,
                user_id=original_audio.user_id,
                filename=new_filename,
                storage_path=path,
                file_type="enhanced",
                file_size_bytes=len(enhanced_bytes),
                duration_seconds=original_audio.duration_seconds, # roughly the same
                sample_rate=target_sr,
                channels=enhanced.shape[0],
                format="wav"
            )
            session.add(enhanced_audio)
            
            job.enhanced_file_id = new_file_id
            job.status = "completed"
            await session.commit()
            logger.info("Database updated and Processing completed")
            
            return {"enhanced_file_id": new_file_id}
            
        except Exception as e:
            logger.error("Processing error with traceback", exc_info=True)
            job.status = "failed"
            job.error_message = str(e)
            await session.commit()
            raise


@celery_app.task(
    bind=True,
    name="worker.tasks.audio_processing.enhance_audio",
    max_retries=2,
    default_retry_delay=30,
)
def enhance_audio(self, job_id: str) -> dict:
    """Process an audio file through the ML enhancement pipeline."""
    logger.info("Starting audio enhancement for job %s", job_id)

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        return loop.run_until_complete(_process_audio(job_id))
    except Exception as exc:
        logger.error("Audio enhancement failed for job %s: %s", job_id, exc)
        raise self.retry(exc=exc)
