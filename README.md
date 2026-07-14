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

**AudioSmith AI** is a sophisticated, full-stack SaaS application that leverages state-of-the-art deep learning to remove background noise from human speech recordings. Built with scalability and performance in mind, it provides a pristine user experience for podcast editors, video producers, and audio engineers.

The ML inference pipeline uses [DeepFilterNet v3](https://github.com/Rikorose/DeepFilterNet) by default, abstracted behind clean interfaces that allow for swappable models, ensuring zero-latency sequential jobs backed by Redis and Celery.

## 🚀 Features

- **Pristine Speech Enhancement**: Removes complex background noise while preserving human voice fidelity.
- **Premium User Interface**: A bespoke Next.js frontend with custom design tokens, glassmorphism aesthetics, and responsive layouts.
- **Asynchronous ML Pipeline**: Celery-backed worker queues ensure the FastAPI HTTP layer never blocks during heavy inference.
- **Visual Audio Analytics**: Real-time waveform rendering for both original and enhanced audio tracking.
- **Bulk Operations**: Intuitive file management with bulk-select and zero-orphan cascading deletions.
- **Secure Architecture**: JWT-based authentication layered over a PostgreSQL database.

## 🧠 System Architecture & Inference Flow

AudioSmith's architecture strictly decouples the web layer from the machine learning inference engine.

1. **Model Loading**: The model weights (`DeepFilterNet3`) are loaded precisely once per Celery worker upon process initialization (`worker_process_init`). A file-lock prevents initialization race conditions. It dynamically binds to a GPU if available (falling back to CPU), retaining the model purely in memory.
2. **Preprocessing**: The `torchaudio` library fetches the raw binary from storage, decodes it, and resamples it to `48kHz` (the required sample rate) while ensuring it is loaded as a `float32` PyTorch tensor. 
3. **Inference**: The worker dispatches the tensor to the `df.enhance` pipeline, which operates asynchronously in the background.
4. **Postprocessing**: The enhanced tensor is peak-normalized (0.99) to prevent clipping. It is encoded back into a `.wav` file securely via Python's `tempfile` memory boundaries before being saved to local storage.

## 💻 Tech Stack

| Layer | Technology |
|:---|:---|
| **Frontend** | Next.js 15, TypeScript, React Context, Vanilla CSS |
| **Backend** | FastAPI, Celery, SQLAlchemy (Async) |
| **Database & Queue** | PostgreSQL, Redis |
| **Machine Learning** | PyTorch, torchaudio, DeepFilterNet |
| **Infrastructure** | Docker, Docker Compose |

## 🛠️ Quick Start (Local Development)

The entire stack is containerized for seamless local deployment.

```bash
# 1. Clone repository
git clone https://github.com/yourusername/AudioSmith.git
cd AudioSmith

# 2. Configure Environment
cp .env.example .env

# 3. Start the Platform
docker compose up --build -d

# 4. Verify Services
docker compose ps
```

The application will be available at:
- **Frontend / Web UI**: [http://localhost:3000](http://localhost:3000)
- **FastAPI OpenAPI Docs**: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

### Asset Management & Storage Strategy

To ensure lightning-fast Git cloning, large binaries (datasets, model checkpoints, processed audio) are **never** committed to the repository. 

**Storage Volumes:**
- `storage/`: (Git Ignored) User-uploaded and AI-enhanced audio files.
- `checkpoints/`: (Git Ignored) Downloaded `.pt` / `.onnx` models.

**Safe Cleanup Command:**
If you wish to free up local disk space or completely wipe data:
```bash
# Wipe database & redis volumes
docker compose down -v

# Clear user audio uploads
rm -rf storage/*

# Clear all local Python caches and Next.js builds
find . -type d \( -name "__pycache__" -o -name ".pytest_cache" -o -name ".ruff_cache" \) -exec rm -rf {} +
rm -rf frontend/.next frontend/out
```

## 🗺️ Roadmap & Future Enhancements
- [ ] Add Conv-TasNet support for benchmarking.
- [ ] Implement chunked streaming for massive audio files.
- [ ] Implement multi-tier user quotas (Free vs Pro).

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
