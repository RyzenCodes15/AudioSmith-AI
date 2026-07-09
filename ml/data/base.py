"""
AudioSmith AI — Base Dataset.

Abstract base class for all audio datasets.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterator, Tuple

import torch


class BaseAudioDataset(ABC):
    """Abstract interface for audio datasets.

    All dataset loaders (LibriSpeech, MUSAN, VoiceBank-DEMAND)
    implement this interface for consistent data access.
    """

    @abstractmethod
    def __len__(self) -> int:
        """Return the number of samples in the dataset."""
        ...

    @abstractmethod
    def __getitem__(self, index: int) -> Tuple[torch.Tensor, int]:
        """Get a single audio sample.

        Args:
            index: Sample index.

        Returns:
            Tuple of (audio_tensor, sample_rate).
        """
        ...

    @abstractmethod
    def get_metadata(self, index: int) -> dict:
        """Get metadata for a sample (speaker, duration, etc.)."""
        ...

    @property
    @abstractmethod
    def sample_rate(self) -> int:
        """Native sample rate of the dataset."""
        ...

    @property
    @abstractmethod
    def root_path(self) -> Path:
        """Root directory of the dataset."""
        ...
