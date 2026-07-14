"""
AudioSmith AI — API v1 Router.

Aggregates all v1 endpoint routers into a single router.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.audio import router as audio_router
from app.api.v1.auth import router as auth_router
from app.api.v1.health import router as health_router
from app.api.v1.processing import router as processing_router

api_v1_router = APIRouter()

# ── Mount sub-routers ───────────────────────────────────────────────────
api_v1_router.include_router(health_router, tags=["Health"])
api_v1_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_v1_router.include_router(audio_router, prefix="/uploads", tags=["Uploads"])
api_v1_router.include_router(processing_router, prefix="/processing", tags=["Processing"])
