"""
AudioSmith AI — Local Filesystem Storage Backend.

Implements the StorageBackend interface using the local filesystem.
Suitable for development and single-server deployments.
"""

from __future__ import annotations

import aiofiles
from pathlib import Path

from app.core.exceptions import StorageError
from app.services.storage.base import StorageBackend


class LocalStorageBackend(StorageBackend):
    """Local filesystem storage implementation.

    Stores files in a configurable directory on the local filesystem.
    For production, replace with S3StorageBackend or GCSStorageBackend.
    """

    def __init__(self, base_path: str) -> None:
        self._base_path = Path(base_path)
        self._base_path.mkdir(parents=True, exist_ok=True)

    def _resolve(self, path: str) -> Path:
        """Resolve a relative path to an absolute filesystem path."""
        resolved = (self._base_path / path).resolve()
        # Prevent path traversal attacks
        if not str(resolved).startswith(str(self._base_path.resolve())):
            raise StorageError("Invalid storage path.")
        return resolved

    async def save(self, path: str, content: bytes) -> str:
        """Save content to the local filesystem."""
        file_path = self._resolve(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(content)
        except OSError as e:
            raise StorageError(f"Failed to save file: {e}")

        return str(path)

    async def load(self, path: str) -> bytes:
        """Load content from the local filesystem."""
        file_path = self._resolve(path)

        if not file_path.exists():
            raise StorageError(f"File not found: '{path}'.")

        try:
            async with aiofiles.open(file_path, "rb") as f:
                return await f.read()
        except OSError as e:
            raise StorageError(f"Failed to read file: {e}")

    async def delete(self, path: str) -> None:
        """Delete a file from the local filesystem."""
        file_path = self._resolve(path)

        if not file_path.exists():
            raise StorageError(f"File not found: '{path}'.")

        try:
            file_path.unlink()
        except OSError as e:
            raise StorageError(f"Failed to delete file: {e}")

    async def exists(self, path: str) -> bool:
        """Check if a file exists on the local filesystem."""
        return self._resolve(path).exists()

    async def get_url(self, path: str) -> str:
        """Get a local file path as a URL."""
        return str(self._resolve(path))
