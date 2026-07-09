"""
AudioSmith AI — Audio Mixer.

Mixes clean speech with noise at target SNR levels
to create training data pairs.
"""

from __future__ import annotations

import torch


class AudioMixer:
    """Mixes clean speech with noise at specified SNR levels.

    Used to create synthetic noisy training data from
    LibriSpeech (clean) + MUSAN (noise) datasets.
    """

    @staticmethod
    def mix(
        clean: torch.Tensor,
        noise: torch.Tensor,
        snr_db: float,
    ) -> torch.Tensor:
        """Mix clean speech with noise at a target SNR.

        Args:
            clean: Clean speech tensor.
            noise: Noise tensor (will be repeated/truncated to match length).
            snr_db: Target signal-to-noise ratio in dB.

        Returns:
            Mixed (noisy) audio tensor.
        """
        # Match noise length to clean length
        clean_len = clean.shape[-1]
        noise_len = noise.shape[-1]

        if noise_len < clean_len:
            # Repeat noise to fill
            repeats = (clean_len // noise_len) + 1
            noise = noise.repeat(1, repeats) if noise.dim() == 2 else noise.repeat(repeats)

        noise = noise[..., :clean_len]

        # Compute scaling factor for target SNR
        clean_power = torch.mean(clean**2)
        noise_power = torch.mean(noise**2)

        if noise_power < 1e-10:
            return clean

        snr_linear = 10 ** (snr_db / 10)
        scale = torch.sqrt(clean_power / (noise_power * snr_linear))

        return clean + scale * noise

    @staticmethod
    def random_snr_mix(
        clean: torch.Tensor,
        noise: torch.Tensor,
        snr_range: tuple[float, float] = (0.0, 20.0),
    ) -> tuple[torch.Tensor, float]:
        """Mix with a random SNR from the given range.

        Args:
            clean: Clean speech tensor.
            noise: Noise tensor.
            snr_range: (min_snr_db, max_snr_db) range.

        Returns:
            Tuple of (mixed_audio, actual_snr_db).
        """
        snr_db = (
            torch.rand(1).item() * (snr_range[1] - snr_range[0])
            + snr_range[0]
        )
        mixed = AudioMixer.mix(clean, noise, snr_db)
        return mixed, snr_db
