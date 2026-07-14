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

        from df.enhance import enhance as df_enhance
        
        # ensure tensor is on the correct device
        audio = audio.to(self._device)
        
        # DeepFilterNet expects float32 tensor
        if audio.dtype != torch.float32:
            audio = audio.to(torch.float32)

        enhanced = df_enhance(self._model, self._df_state, audio)
        return enhanced

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

        import sys
        import types
        import torchaudio
        
        # Monkeypatch torchaudio.backend.common for deepfilternet compatibility with torchaudio >= 2.4.0
        if "torchaudio.backend.common" not in sys.modules:
            backend = types.ModuleType('torchaudio.backend')
            common = types.ModuleType('torchaudio.backend.common')
            common.AudioMetaData = getattr(torchaudio, 'AudioMetaData', type('AudioMetaData', (), {}))
            backend.common = common
            sys.modules['torchaudio.backend'] = backend
            sys.modules['torchaudio.backend.common'] = common
            
        from df.enhance import init_df, enhance
        
        # init_df(model_base_dir, config_allow_defaults)
        # We can pass None to download/use default pretrained
        import fcntl
        import os
        lock_file = os.path.expanduser("~/.cache/download.lock")
        os.makedirs(os.path.dirname(lock_file), exist_ok=True)
        with open(lock_file, "w") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                self._model, self._df_state, _ = init_df()
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
        
        # Determine device dynamically
        if torch.cuda.is_available():
            self._device = "cuda"
        else:
            self._device = "cpu"
            
        self._model = self._model.to(self._device)
        self._loaded = True
        logger.info(f"Model loaded successfully. Device selected: {self._device}. Model version: DeepFilterNet3")

    def to_device(self, device: str) -> "DeepFilterNetAdapter":
        """Move model to device."""
        self._device = device
        if self._loaded and self._model is not None:
            self._model = self._model.to(device)
        return self

    @property
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self._loaded
