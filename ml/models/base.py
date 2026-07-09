"""
AudioSmith AI — Base Speech Enhancer.

Abstract base class that all speech enhancement models must implement.
This is the core abstraction that enables model swapping without
changing any business logic, preprocessing, or serving code.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

import torch


class BaseSpeechEnhancer(ABC):
    """Abstract interface for speech enhancement models.

    Every model adapter (DeepFilterNet, Conv-TasNet, etc.) implements
    this interface. The rest of the system depends only on this ABC,
    never on concrete model implementations.

    Usage:
        model = registry.get("deepfilternet")
        model.load()
        enhanced = model.enhance(noisy_audio)
    """

    @abstractmethod
    def enhance(self, audio: torch.Tensor) -> torch.Tensor:
        """Enhance a noisy audio tensor.

        Args:
            audio: Input audio tensor of shape (channels, samples)
                   at the model's expected sample rate.

        Returns:
            Enhanced audio tensor of same shape.
        """
        ...

    @abstractmethod
    def get_sample_rate(self) -> int:
        """Get the sample rate expected by this model.

        Returns:
            Sample rate in Hz (e.g., 48000 for DeepFilterNet).
        """
        ...

    @abstractmethod
    def get_model_name(self) -> str:
        """Get the human-readable model name.

        Returns:
            Model name string (e.g., "DeepFilterNet3").
        """
        ...

    @abstractmethod
    def load(self, checkpoint_path: Optional[str] = None) -> None:
        """Load model weights.

        Args:
            checkpoint_path: Optional path to a checkpoint file.
                           If None, uses the default pre-trained weights.
        """
        ...

    @abstractmethod
    def to_device(self, device: str) -> "BaseSpeechEnhancer":
        """Move the model to a specific device.

        Args:
            device: Target device ("cpu", "cuda", "cuda:0", etc.).

        Returns:
            Self for method chaining.
        """
        ...

    @property
    @abstractmethod
    def is_loaded(self) -> bool:
        """Check if the model weights are loaded and ready for inference."""
        ...
