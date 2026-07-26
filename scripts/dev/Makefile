# ============================================================================
# AudioSmith AI — Makefile
# ============================================================================
# Developer ergonomics for common tasks.
# Usage: make <target>
# ============================================================================

.PHONY: help dev dev-backend dev-frontend dev-worker install install-backend install-frontend lint lint-backend lint-frontend test test-backend test-frontend docker-up docker-down docker-build db-migrate db-upgrade db-downgrade clean

# Default target
help: ## Show this help message
	@echo "AudioSmith AI — Available Commands"
	@echo "=================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ---------------------------------------------------------------------------
# Installation
# ---------------------------------------------------------------------------

install: install-backend install-frontend ## Install all dependencies

install-backend: ## Install backend dependencies
	cd backend && pip install -e ".[dev]"

install-frontend: ## Install frontend dependencies
	cd frontend && npm install

# ---------------------------------------------------------------------------
# Development
# ---------------------------------------------------------------------------

dev: ## Start all services (docker compose)
	docker compose up -d

dev-backend: ## Start backend dev server
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Start frontend dev server
	cd frontend && npm run dev

dev-worker: ## Start Celery worker
	cd backend && celery -A worker.celery_app worker --loglevel=info

# ---------------------------------------------------------------------------
# Testing
# ---------------------------------------------------------------------------

test: test-backend test-frontend ## Run all tests

test-backend: ## Run backend tests
	cd backend && pytest -v

test-frontend: ## Run frontend tests
	cd frontend && npm test

# ---------------------------------------------------------------------------
# Linting & Formatting
# ---------------------------------------------------------------------------

lint: lint-backend lint-frontend ## Run all linters

lint-backend: ## Lint backend code
	cd backend && ruff check . && ruff format --check .

lint-frontend: ## Lint frontend code
	cd frontend && npm run lint

format-backend: ## Format backend code
	cd backend && ruff format .

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

db-migrate: ## Create a new migration (usage: make db-migrate msg="description")
	cd backend && alembic revision --autogenerate -m "$(msg)"

db-upgrade: ## Apply all pending migrations
	cd backend && alembic upgrade head

db-downgrade: ## Rollback last migration
	cd backend && alembic downgrade -1

# ---------------------------------------------------------------------------
# Docker
# ---------------------------------------------------------------------------

docker-build: ## Build all Docker images
	docker compose build

docker-up: ## Start all containers
	docker compose up -d

docker-down: ## Stop all containers
	docker compose down

docker-logs: ## Tail logs from all containers
	docker compose logs -f

# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------

clean: ## Remove build artifacts, caches, and temporary files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name node_modules -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .next -exec rm -rf {} + 2>/dev/null || true
	rm -rf dist/ build/ *.egg-info/
