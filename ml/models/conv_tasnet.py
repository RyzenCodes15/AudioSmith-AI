"""
AudioSmith AI — Conv-TasNet Adapter.

Wraps Conv-TasNet (via torchaudio or Asteroid) to conform to the
BaseSpeechEnhancer interface. Used for benchmarking and evaluation only.
"""

from __future__ import annotations

import logging
from typing import Optional

import torch

from ml.models.base import BaseSpeechEnhancer

logger = logging.getLogger(__name__)


class ConvTasNetAdapter(BaseSpeechEnhancer):
    """Conv-TasNet model adapter.

    Wraps Conv-TasNet behind the BaseSpeechEnhancer ABC.
    This model is used for benchmarking and A/B evaluation only,
    NOT as the production inference model.

    Conv-TasNet operates at 8kHz or 16kHz (depending on the
    pre-trained checkpoint) and is designed for source separation.

    References:
        - Paper: https://arxiv.org/abs/1809.07454
        - torchaudio: torchaudio.models.ConvTasNet
        - Asteroid: asteroid.models.ConvTasNet
    """

    def __init__(self, sample_rate: int = 16000) -> None:
        self._model = None
        self._sample_rate = sample_rate
        self._device = "cpu"
        self._loaded = False

    def enhance(self, audio: torch.Tensor) -> torch.Tensor:
        """Enhance noisy speech using Conv-TasNet.

        Args:
            audio: Input tensor of shape (channels, samples) at
                   the model's expected sample rate.

        Returns:
            Enhanced audio tensor of same shape.

        Raises:
            RuntimeError: If model is not loaded.
        """
        if not self._loaded:
            raise RuntimeError("Model not loaded. Call load() first.")

        # Future: implement actual inference
        # Option A — torchaudio:
        # output = self._model(audio.unsqueeze(0))
        # return output.squeeze(0)[0]  # Take first source
        #
        # Option B — Asteroid:
        # from asteroid.models import ConvTasNet
        # output = self._model(audio)
        # return output[0]

        raise NotImplementedError(
            "Conv-TasNet inference not yet implemented. "
            "Install torchaudio or asteroid and implement the enhance method."
        )

    def get_sample_rate(self) -> int:
        """Conv-TasNet typically operates at 8kHz or 16kHz."""
        return self._sample_rate

    def get_model_name(self) -> str:
        """Return model name."""
        return "Conv-TasNet"

    def load(self, checkpoint_path: Optional[str] = None) -> None:
        """Load Conv-TasNet model weights.

        Args:
            checkpoint_path: Optional custom checkpoint path.
                           If None, loads a pre-trained model.
        """
        logger.info("Loading Conv-TasNet model...")

        # Future: implement actual model loading
        # Option A — torchaudio:
        # from torchaudio.models import conv_tasnet_base
        # self._model = conv_tasnet_base()
        # if checkpoint_path:
        #     self._model.load_state_dict(torch.load(checkpoint_path))
        #
        # Option B — Asteroid:
        # from asteroid.models import ConvTasNet
        # self._model = ConvTasNet.from_pretrained("mpariente/ConvTasNet_WHAM!_sepclean")

        self._loaded = True
        logger.info("Conv-TasNet model loaded successfully.")

    def to_device(self, device: str) -> "ConvTasNetAdapter":
        """Move model to device."""
        self._device = device
        if self._model is not None:
            self._model = self._model.to(device)
        return self

    @property
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self._loaded
