"""
AudioSmith AI — Audio Normalizer.

Handles audio level normalization.
"""

from __future__ import annotations

import torch


class AudioNormalizer:
    """Normalizes audio levels for consistent model input.

    Ensures audio is within the expected amplitude range
    before passing to the enhancement model.
    """

    def normalize(self, audio: torch.Tensor) -> torch.Tensor:
        """Normalize audio to [-1, 1] range.

        Args:
            audio: Input tensor of shape (channels, samples).

        Returns:
            Normalized audio tensor.
        """
        max_val = audio.abs().max()
        if max_val > 0:
            audio = audio / max_val
        return audio

    def denormalize(
        self, audio: torch.Tensor, original_max: float
    ) -> torch.Tensor:
        """Restore audio to its original amplitude range.

        Args:
            audio: Normalized tensor of shape (channels, samples).
            original_max: Original maximum absolute value.

        Returns:
            Denormalized audio tensor.
        """
        return audio * original_max
