"""
AudioSmith AI — Custom Exception Hierarchy.

All application-specific exceptions inherit from AudioSmithError.
Each exception maps to an appropriate HTTP status code.
"""

from __future__ import annotations


class AudioSmithError(Exception):
    """Base exception for all AudioSmith errors."""

    def __init__(self, message: str = "An unexpected error occurred.") -> None:
        self.message = message
        super().__init__(self.message)


# ── Authentication & Authorization ──────────────────────────────────────


class AuthenticationError(AudioSmithError):
    """Raised when authentication fails (401)."""

    def __init__(self, message: str = "Invalid credentials.") -> None:
        super().__init__(message)


class AuthorizationError(AudioSmithError):
    """Raised when user lacks permission (403)."""

    def __init__(self, message: str = "Insufficient permissions.") -> None:
        super().__init__(message)


# ── Resource Errors ─────────────────────────────────────────────────────


class NotFoundError(AudioSmithError):
    """Raised when a requested resource is not found (404)."""

    def __init__(self, resource: str = "Resource", identifier: str = "") -> None:
        message = f"{resource} not found."
        if identifier:
            message = f"{resource} '{identifier}' not found."
        super().__init__(message)


class ConflictError(AudioSmithError):
    """Raised when a resource already exists (409)."""

    def __init__(self, message: str = "Resource already exists.") -> None:
        super().__init__(message)


# ── Validation Errors ───────────────────────────────────────────────────


class ValidationError(AudioSmithError):
    """Raised when input validation fails (422)."""

    def __init__(self, message: str = "Validation failed.") -> None:
        super().__init__(message)


# ── Audio Processing Errors ─────────────────────────────────────────────


class AudioProcessingError(AudioSmithError):
    """Raised when audio processing fails (500)."""

    def __init__(self, message: str = "Audio processing failed.") -> None:
        super().__init__(message)


class UnsupportedAudioFormatError(ValidationError):
    """Raised when the audio format is not supported (422)."""

    def __init__(self, format: str = "unknown") -> None:
        super().__init__(f"Unsupported audio format: '{format}'.")


class AudioTooLongError(ValidationError):
    """Raised when audio exceeds maximum duration (422)."""

    def __init__(self, duration: float, max_duration: float) -> None:
        super().__init__(
            f"Audio duration ({duration:.1f}s) exceeds maximum "
            f"allowed duration ({max_duration:.1f}s)."
        )


# ── Storage Errors ──────────────────────────────────────────────────────


class StorageError(AudioSmithError):
    """Raised when a storage operation fails (500)."""

    def __init__(self, message: str = "Storage operation failed.") -> None:
        super().__init__(message)
