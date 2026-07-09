# ============================================================================
# AudioSmith AI — Worker Dockerfile
# ============================================================================

FROM python:3.11-slim

WORKDIR /app

# System dependencies (same as backend + ML libraries)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY backend/pyproject.toml .
RUN pip install --no-cache-dir -e "."

# Application code
COPY backend/ .
COPY ml/ ./ml/

CMD ["celery", "-A", "worker.celery_app", "worker", "--loglevel=info", "--queues=audio"]
