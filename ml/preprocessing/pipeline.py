"""
AudioSmith AI — Preprocessing Pipeline.

Orchestrates audio preprocessing steps before model inference.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import torch

from ml.preprocessing.normalizer import AudioNormalizer
from ml.preprocessing.resampler import AudioResampler
from ml.preprocessing.validator import AudioValidator

logger = logging.getLogger(__name__)


@dataclass
class PreprocessingResult:
    """Result of the preprocessing pipeline."""

    audio: torch.Tensor
    original_sample_rate: int
    target_sample_rate: int
    duration_seconds: float
    was_resampled: bool


class PreprocessingPipeline:
    """Orchestrates audio preprocessing before model inference.

    Pipeline steps:
    1. Validate audio format and duration
    2. Resample to model's expected sample rate
    3. Normalize audio levels
    """

    def __init__(
        self,
        target_sample_rate: int = 48000,
        max_duration_seconds: int = 300,
    ) -> None:
        self._validator = AudioValidator(max_duration_seconds=max_duration_seconds)
        self._resampler = AudioResampler(target_sample_rate=target_sample_rate)
        self._normalizer = AudioNormalizer()
        self._target_sr = target_sample_rate

    def process(
        self, audio: torch.Tensor, sample_rate: int
    ) -> PreprocessingResult:
        """Run the full preprocessing pipeline.

        Args:
            audio: Raw audio tensor (channels, samples).
            sample_rate: Original sample rate of the audio.

        Returns:
            PreprocessingResult with processed audio and metadata.

        Raises:
            ValidationError: If audio fails validation checks.
        """
        logger.info(
            "Preprocessing: sr=%d, shape=%s", sample_rate, audio.shape
        )

        # Step 1: Validate
        duration = audio.shape[-1] / sample_rate
        self._validator.validate(audio, sample_rate)

        # Step 2: Resample if necessary
        was_resampled = sample_rate != self._target_sr
        if was_resampled:
            audio = self._resampler.resample(audio, sample_rate)

        # Step 3: Normalize
        audio = self._normalizer.normalize(audio)

        return PreprocessingResult(
            audio=audio,
            original_sample_rate=sample_rate,
            target_sample_rate=self._target_sr,
            duration_seconds=duration,
            was_resampled=was_resampled,
        )
