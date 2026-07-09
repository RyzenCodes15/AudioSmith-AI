"""
AudioSmith AI — VoiceBank-DEMAND Dataset Loader.

Loads paired clean/noisy samples for evaluation.
This is the standard benchmark for speech enhancement.
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import torch

from ml.data.base import BaseAudioDataset


class VoiceBankDEMANDDataset(BaseAudioDataset):
    """VoiceBank-DEMAND dataset loader.

    Loads paired (clean, noisy) utterances for evaluation.
    The test set uses 2 unseen speakers with unseen noise types.

    Dataset structure:
        VoiceBank-DEMAND/
        ├── clean_trainset_28spk_wav/
        ├── noisy_trainset_28spk_wav/
        ├── clean_testset_wav/
        └── noisy_testset_wav/

    References:
        - Valentini et al. (2016)
    """

    def __init__(
        self,
        root: str | Path,
        split: str = "test",
    ) -> None:
        self._root = Path(root) / "VoiceBank-DEMAND"
        self._split = split

        if split == "test":
            self._clean_dir = self._root / "clean_testset_wav"
            self._noisy_dir = self._root / "noisy_testset_wav"
        else:
            self._clean_dir = self._root / "clean_trainset_28spk_wav"
            self._noisy_dir = self._root / "noisy_trainset_28spk_wav"

        self._file_list: list[str] = []
        if self._clean_dir.exists():
            self._file_list = sorted(
                f.stem for f in self._clean_dir.glob("*.wav")
            )

    def __len__(self) -> int:
        return len(self._file_list)

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, int]:
        # Future: returns (clean, noisy) pair
        # clean_path = self._clean_dir / f"{self._file_list[index]}.wav"
        # noisy_path = self._noisy_dir / f"{self._file_list[index]}.wav"
        # clean, sr = torchaudio.load(clean_path)
        # noisy, _ = torchaudio.load(noisy_path)
        # return clean, noisy, sr
        raise NotImplementedError("VoiceBank-DEMAND loading requires torchaudio.")

    def get_pair(self, index: int) -> Tuple[torch.Tensor, torch.Tensor, int]:
        """Get a (clean, noisy) pair for evaluation.

        Returns:
            Tuple of (clean_audio, noisy_audio, sample_rate).
        """
        raise NotImplementedError("VoiceBank-DEMAND pair loading not yet implemented.")

    def get_metadata(self, index: int) -> dict:
        return {
            "utterance_id": self._file_list[index],
            "split": self._split,
        }

    @property
    def sample_rate(self) -> int:
        return 16000

    @property
    def root_path(self) -> Path:
        return self._root
