"""
AudioSmith AI — LibriSpeech Dataset Loader.

Loads clean speech samples from the LibriSpeech corpus.
Used as the clean speech source for training data creation.
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import torch

from ml.data.base import BaseAudioDataset


class LibriSpeechDataset(BaseAudioDataset):
    """LibriSpeech dataset loader.

    Loads clean speech from LibriSpeech for creating noisy training pairs.
    Supports train-clean-100, train-clean-360, dev-clean, test-clean splits.

    Dataset structure:
        LibriSpeech/
        ├── train-clean-100/
        │   └── <speaker_id>/
        │       └── <chapter_id>/
        │           ├── <utterance_id>.flac
        │           └── <speaker_id>-<chapter_id>.trans.txt
        ├── train-clean-360/
        ├── dev-clean/
        └── test-clean/

    References:
        - https://www.openslr.org/12/
    """

    SPLITS = ["train-clean-100", "train-clean-360", "dev-clean", "test-clean"]

    def __init__(
        self,
        root: str | Path,
        split: str = "train-clean-100",
    ) -> None:
        self._root = Path(root) / "LibriSpeech" / split
        self._split = split
        self._file_list: list[Path] = []

        if self._root.exists():
            self._file_list = sorted(self._root.rglob("*.flac"))

    def __len__(self) -> int:
        return len(self._file_list)

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, int]:
        # Future: load with torchaudio
        # audio, sr = torchaudio.load(self._file_list[index])
        # return audio, sr
        raise NotImplementedError("LibriSpeech loading requires torchaudio.")

    def get_metadata(self, index: int) -> dict:
        path = self._file_list[index]
        parts = path.stem.split("-")
        return {
            "path": str(path),
            "speaker_id": parts[0] if len(parts) >= 1 else "unknown",
            "chapter_id": parts[1] if len(parts) >= 2 else "unknown",
            "utterance_id": path.stem,
        }

    @property
    def sample_rate(self) -> int:
        return 16000

    @property
    def root_path(self) -> Path:
        return self._root
