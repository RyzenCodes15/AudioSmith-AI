# AudioSmith AI 🎙️✨

<div align="center">
  <p><strong>Production-grade AI SaaS for professional speech enhancement.</strong></p>
  
  ![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
  ![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi)
  ![Next.js](https://img.shields.io/badge/Next.js-15-000000.svg?logo=next.js)
  ![PyTorch](https://img.shields.io/badge/PyTorch-2.4+-EE4C2C.svg?logo=pytorch)
  ![License](https://img.shields.io/badge/license-MIT-green.svg)
</div>

---

## Overview

AudioSmith AI is a sophisticated AI-powered SaaS application that removes background noise from human speech recordings. It is engineered as a full-stack, scalable product featuring a modern web interface and a robust asynchronous processing backend.

The ML inference pipeline uses [DeepFilterNet](https://github.com/Rikorose/DeepFilterNet) by default, abstracted behind clean interfaces that allow for swappable models (e.g., Conv-TasNet for benchmarking).

## Features

- **High-Quality Speech Enhancement**: Removes background noise while preserving voice clarity.
- **Modern User Interface**: Feature-driven Next.js frontend with custom design tokens.
- **Asynchronous Processing**: Celery-backed worker queue prevents API blocking.
- **Audio Visualizations**: Automatically generates waveform and spectrogram comparisons.
- **Clean Architecture**: Backend and ML layers are highly decoupled using abstractions.

## AI Inference Flow

AudioSmith's core functionality relies on DeepFilterNet. The end-to-end processing guarantees high fidelity results:
1. **Model Loading**: The model weights are loaded precisely once per Celery worker upon process initialization (`worker_process_init`). A file-lock prevents race conditions. It dynamically binds to a GPU if available, or falls back to the CPU, retaining the model purely in memory for zero-latency sequential jobs.
2. **Preprocessing**: The `torchaudio` library fetches the raw binary, decodes it, and resamples it to `48kHz` (DeepFilterNet's required sample rate) while ensuring it is loaded as a `float32` PyTorch tensor. 
3. **Inference**: The worker dispatches the tensor to the `df.enhance` pipeline, which operates seamlessly in the background without blocking the FastAPI HTTP event loop.
4. **Postprocessing**: The enhanced tensor is peak-normalized (0.99) to prevent clipping. It is then encoded back into a `.wav` file securely via Python's `tempfile` memory boundaries before being saved to local storage.

## Tech Stack

| Layer | Technology |
|:---|:---|
| **Frontend** | Next.js 15, TypeScript, Vanilla CSS |
| **Backend** | FastAPI, Celery, SQLAlchemy (Async) |
| **Database & Queue** | PostgreSQL, Redis |
| **Machine Learning** | PyTorch, torchaudio, DeepFilterNet |
| **Infrastructure** | Docker, Docker Compose |

## Quick Start (Local Development)

The easiest way to run the entire stack locally is via Docker Compose.

```bash
# 1. Clone repository
git clone https://github.com/yourusername/AudioSmith.git
cd AudioSmith

# 2. Copy .env.example to .env
cp .env.example .env

# 3. Install dependencies (if required)
# Frontend dependencies are installed in the container, but you can install them locally for IDE support:
# cd frontend && npm install && cd ..

# 4. Run docker compose up --build
docker compose up --build -d

# 5. Verify application startup
docker compose ps
```

### Asset Management & Storage Strategy
To keep the repository lightweight and cloning fast, large binaries (datasets, model checkpoints, processed audio) are **never** committed to Git. Instead, they are managed externally via scripts and configured via environment variables.

To fetch required external assets (if any are needed for offline ML model loading or datasets), run:
```bash
./scripts/download_assets.sh
```

**Storage Locations:**
- `storage/`: (Ignored in Git) Where user-uploaded and AI-enhanced audio files are saved locally.
- `checkpoints/`: (Ignored in Git) Where downloaded `.pt` / `.onnx` models are stored.
- `datasets/`: (Ignored in Git) Where large `.zip` / `.tar.gz` datasets go.

**Safe Cleanup:**
If you wish to free up local disk space or wipe data:
```bash
# Wipe database & redis data
docker compose down -v

# Clear user audio uploads
rm -rf storage/*

# Clear all local Python caches and Next.js builds
find . -type d \( -name "__pycache__" -o -name ".pytest_cache" -o -name ".ruff_cache" \) -exec rm -rf {} +
rm -rf frontend/.next frontend/out
```

### Environment Variables

If you need to configure upload limits, modify these in your `.env`:
- `UPLOAD_MAX_SIZE_BYTES` (default: 52428800 for 50MB)
- `UPLOAD_ALLOWED_EXTENSIONS` (default: `[".wav",".mp3",".flac"]`)

The application will be available at:
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/api/docs

## Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [Contributing Guidelines](CONTRIBUTING.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
