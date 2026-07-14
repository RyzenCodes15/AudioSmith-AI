# ============================================================================
# AudioSmith AI — Worker Dockerfile
# ============================================================================

FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsndfile1 \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch CPU first to avoid downloading 4GB+ CUDA binaries
RUN pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# Python dependencies
COPY backend/pyproject.toml .
COPY ml/pyproject.toml ./ml/
RUN pip install --no-cache-dir "./ml" "."

# Application code (only copy necessary folders to avoid caching logs/tests)
COPY backend/alembic.ini ./
COPY backend/app/ ./app/
COPY backend/worker/ ./worker/
COPY ml/config.py ml/__init__.py ./ml/
COPY ml/configs/ ./ml/configs/
COPY ml/models/ ./ml/models/
COPY ml/postprocessing/ ./ml/postprocessing/
COPY ml/preprocessing/ ./ml/preprocessing/

CMD ["celery", "-A", "worker.celery_app", "worker", "--loglevel=info", "--queues=audio"]
