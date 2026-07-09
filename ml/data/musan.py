"""
AudioSmith AI — MUSAN Dataset Loader.

Loads noise samples from the MUSAN corpus.
Used as the noise source for creating noisy training pairs.
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import torch

from ml.data.base import BaseAudioDataset


class MUSANDataset(BaseAudioDataset):
    """MUSAN dataset loader.

    Loads noise clips from MUSAN for mixing with clean speech.
    Supports noise, music, and speech categories.

    Dataset structure:
        musan/
        ├── noise/
        │   ├── free-sound/
        │   └── sound-bible/
        ├── music/
        └── speech/

    References:
        - https://www.openslr.org/17/
    """

    CATEGORIES = ["noise", "music", "speech"]

    def __init__(
        self,
        root: str | Path,
        category: str = "noise",
    ) -> None:
        self._root = Path(root) / "musan" / category
        self._category = category
        self._file_list: list[Path] = []

        if self._root.exists():
            self._file_list = sorted(self._root.rglob("*.wav"))

    def __len__(self) -> int:
        return len(self._file_list)

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, int]:
        # Future: load with torchaudio
        # audio, sr = torchaudio.load(self._file_list[index])
        # return audio, sr
        raise NotImplementedError("MUSAN loading requires torchaudio.")

    def get_metadata(self, index: int) -> dict:
        path = self._file_list[index]
        return {
            "path": str(path),
            "category": self._category,
            "filename": path.name,
        }

    @property
    def sample_rate(self) -> int:
        return 16000

    @property
    def root_path(self) -> Path:
        return self._root
