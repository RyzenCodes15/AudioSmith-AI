"""
AudioSmith AI — Audio Validator.

Validates audio files before processing.
"""

from __future__ import annotations

import torch


class AudioValidator:
    """Validates audio files before they enter the processing pipeline.

    Checks:
    - Duration is within limits
    - Audio is not silent
    - Tensor shape is valid
    """

    SUPPORTED_FORMATS = {"wav", "mp3", "flac", "ogg", "m4a"}

    def __init__(self, max_duration_seconds: int = 300) -> None:
        self._max_duration = max_duration_seconds

    def validate(self, audio: torch.Tensor, sample_rate: int) -> None:
        """Validate an audio tensor.

        Args:
            audio: Audio tensor of shape (channels, samples).
            sample_rate: Sample rate in Hz.

        Raises:
            ValueError: If validation fails.
        """
        # Check tensor is not empty
        if audio.numel() == 0:
            raise ValueError("Audio tensor is empty.")

        # Check dimensions
        if audio.dim() not in (1, 2):
            raise ValueError(
                f"Expected 1D or 2D tensor, got {audio.dim()}D."
            )

        # Check duration
        num_samples = audio.shape[-1]
        duration = num_samples / sample_rate
        if duration > self._max_duration:
            raise ValueError(
                f"Audio duration ({duration:.1f}s) exceeds maximum "
                f"allowed duration ({self._max_duration}s)."
            )

        # Check for silence (all zeros)
        if audio.abs().max() < 1e-7:
            raise ValueError("Audio appears to be silent.")

    @classmethod
    def validate_format(cls, filename: str) -> None:
        """Validate audio file format by extension.

        Args:
            filename: Name of the audio file.

        Raises:
            ValueError: If format is not supported.
        """
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if ext not in cls.SUPPORTED_FORMATS:
            supported = ", ".join(sorted(cls.SUPPORTED_FORMATS))
            raise ValueError(
                f"Unsupported format '{ext}'. Supported: {supported}"
            )
