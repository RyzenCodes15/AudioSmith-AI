"""
AudioSmith AI — Storage Backend Abstract Base Class.

Defines the interface that all storage implementations must follow.
This enables swapping between local filesystem, S3, GCS, etc.
without changing any business logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class StorageBackend(ABC):
    """Abstract storage backend interface.

    All storage implementations (local, S3, GCS) must implement
    these methods. Business logic depends only on this interface.
    """

    @abstractmethod
    async def save(self, path: str, content: bytes) -> str:
        """Save content to storage.

        Args:
            path: Relative path within the storage system.
            content: Raw bytes to store.

        Returns:
            The storage path/URL where the content was saved.
        """
        ...

    @abstractmethod
    async def load(self, path: str) -> bytes:
        """Load content from storage.

        Args:
            path: Relative path within the storage system.

        Returns:
            Raw bytes of the stored content.

        Raises:
            StorageError: If the file doesn't exist or can't be read.
        """
        ...

    @abstractmethod
    async def delete(self, path: str) -> None:
        """Delete content from storage.

        Args:
            path: Relative path within the storage system.

        Raises:
            StorageError: If the file doesn't exist or can't be deleted.
        """
        ...

    @abstractmethod
    async def exists(self, path: str) -> bool:
        """Check if content exists in storage.

        Args:
            path: Relative path within the storage system.

        Returns:
            True if the content exists.
        """
        ...

    @abstractmethod
    async def get_url(self, path: str) -> str:
        """Get a URL for accessing the stored content.

        Args:
            path: Relative path within the storage system.

        Returns:
            A URL (local path or presigned URL) for the content.
        """
        ...
