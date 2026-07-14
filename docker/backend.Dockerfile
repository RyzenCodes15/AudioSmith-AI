# ============================================================================
# AudioSmith AI — Backend Dockerfile
# ============================================================================

FROM python:3.11-slim

WORKDIR /app

# System dependencies (removed ffmpeg and libsndfile1 as API does not process audio)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY backend/pyproject.toml .
RUN pip install --no-cache-dir "."

# Application code
COPY backend/alembic.ini ./
COPY backend/app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
