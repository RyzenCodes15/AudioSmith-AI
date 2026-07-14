# ============================================================================
# AudioSmith AI — Worker Dockerfile
# ============================================================================

FROM python:3.11-slim

WORKDIR /app

# System dependencies (same as backend + ML libraries)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsndfile1 \
    ffmpeg \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY backend/pyproject.toml .
COPY ml/pyproject.toml ./ml/
RUN pip install --no-cache-dir "./ml" "."

# Application code
COPY backend/ .
COPY ml/ ./ml/

CMD ["celery", "-A", "worker.celery_app", "worker", "--loglevel=info", "--queues=audio"]
