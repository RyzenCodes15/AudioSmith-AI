"""
AudioSmith AI — Middleware.

Custom middleware for request logging, exception handling, etc.
"""

from __future__ import annotations

import logging
import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    AudioSmithError,
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    NotFoundError,
    ValidationError,
)

logger = logging.getLogger(__name__)


# ── Exception-to-HTTP Status Code Mapping ────────────────────────────────

EXCEPTION_STATUS_MAP: dict[type[AudioSmithError], int] = {
    AuthenticationError: 401,
    AuthorizationError: 403,
    NotFoundError: 404,
    ConflictError: 409,
    ValidationError: 422,
}


def register_exception_handlers(app: FastAPI) -> None:
    """Register custom exception handlers on the FastAPI app."""

    @app.exception_handler(AudioSmithError)
    async def audiosmith_error_handler(
        request: Request, exc: AudioSmithError
    ) -> JSONResponse:
        status_code = EXCEPTION_STATUS_MAP.get(type(exc), 500)
        return JSONResponse(
            status_code=status_code,
            content={
                "error": type(exc).__name__,
                "message": exc.message,
            },
        )


def register_request_logging(app: FastAPI) -> None:
    """Register middleware for request/response logging."""

    @app.middleware("http")
    async def log_requests(
        request: Request, call_next: Callable[[Request], Response]
    ) -> Response:
        start_time = time.perf_counter()

        response = await call_next(request)

        duration_ms = (time.perf_counter() - start_time) * 1000
        logger.info(
            "%s %s → %d (%.1fms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )

        return response
