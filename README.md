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

The application will be available at:
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/api/docs

## Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [Contributing Guidelines](CONTRIBUTING.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
