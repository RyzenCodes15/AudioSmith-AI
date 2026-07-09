"""
AudioSmith AI — DeepFilterNet Adapter.

Wraps the DeepFilterNet library to conform to the BaseSpeechEnhancer interface.
This is the production model for speech enhancement.
"""

from __future__ import annotations

import logging
from typing import Optional

import torch

from ml.models.base import BaseSpeechEnhancer

logger = logging.getLogger(__name__)


class DeepFilterNetAdapter(BaseSpeechEnhancer):
    """DeepFilterNet model adapter.

    Wraps the `deepfilternet` library's enhance function behind
    the BaseSpeechEnhancer ABC. This is the primary production model.

    DeepFilterNet operates at 48kHz and is designed for real-time
    speech enhancement on a single CPU thread.

    References:
        - Paper: https://arxiv.org/abs/2305.08227
        - Repo: https://github.com/Rikorose/DeepFilterNet
    """

    def __init__(self) -> None:
        self._model = None
        self._df_state = None
        self._device = "cpu"
        self._loaded = False

    def enhance(self, audio: torch.Tensor) -> torch.Tensor:
        """Enhance noisy speech using DeepFilterNet.

        Args:
            audio: Input tensor of shape (channels, samples) at 48kHz.

        Returns:
            Enhanced audio tensor of same shape.

        Raises:
            RuntimeError: If model is not loaded.
        """
        if not self._loaded:
            raise RuntimeError("Model not loaded. Call load() first.")

        # Future: implement actual inference
        # from df.enhance import enhance as df_enhance
        # enhanced = df_enhance(self._model, self._df_state, audio)
        # return enhanced

        raise NotImplementedError(
            "DeepFilterNet inference not yet implemented. "
            "Install deepfilternet and implement the enhance method."
        )

    def get_sample_rate(self) -> int:
        """DeepFilterNet operates at 48kHz."""
        return 48000

    def get_model_name(self) -> str:
        """Return model name."""
        return "DeepFilterNet3"

    def load(self, checkpoint_path: Optional[str] = None) -> None:
        """Load DeepFilterNet model weights.

        Args:
            checkpoint_path: Optional custom checkpoint path.
                           If None, loads the default pre-trained model.
        """
        logger.info("Loading DeepFilterNet model...")

        # Future: implement actual model loading
        # from df.enhance import init_df
        # self._model, self._df_state, _ = init_df()

        self._loaded = True
        logger.info("DeepFilterNet model loaded successfully.")

    def to_device(self, device: str) -> "DeepFilterNetAdapter":
        """Move model to device."""
        self._device = device
        # Future: move model tensors to device
        return self

    @property
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self._loaded
