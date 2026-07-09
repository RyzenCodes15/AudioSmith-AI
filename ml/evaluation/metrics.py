"""
AudioSmith AI — Audio Quality Metrics.

Implements standard speech enhancement evaluation metrics:
- PESQ (Perceptual Evaluation of Speech Quality)
- STOI (Short-Time Objective Intelligibility)
- SI-SDR (Scale-Invariant Signal-to-Distortion Ratio)
- SNR (Signal-to-Noise Ratio)
"""

from __future__ import annotations

from dataclasses import dataclass

import torch


@dataclass
class QualityMetrics:
    """Container for audio quality evaluation metrics."""

    pesq: float | None = None
    stoi: float | None = None
    si_sdr: float | None = None
    snr: float | None = None

    def to_dict(self) -> dict:
        """Convert to dictionary, excluding None values."""
        return {k: v for k, v in self.__dict__.items() if v is not None}


def compute_si_sdr(
    reference: torch.Tensor, estimated: torch.Tensor
) -> float:
    """Compute Scale-Invariant Signal-to-Distortion Ratio.

    Args:
        reference: Clean reference signal.
        estimated: Enhanced/estimated signal.

    Returns:
        SI-SDR in dB.
    """
    reference = reference.flatten()
    estimated = estimated.flatten()

    # Zero-mean
    reference = reference - reference.mean()
    estimated = estimated - estimated.mean()

    # SI-SDR computation
    dot = torch.dot(reference, estimated)
    s_target = dot * reference / torch.dot(reference, reference)
    e_noise = estimated - s_target

    si_sdr = 10 * torch.log10(
        torch.dot(s_target, s_target) / torch.dot(e_noise, e_noise)
    )

    return si_sdr.item()


def compute_snr(
    reference: torch.Tensor, noise: torch.Tensor
) -> float:
    """Compute Signal-to-Noise Ratio.

    Args:
        reference: Clean reference signal.
        noise: Noise signal (or estimated - reference).

    Returns:
        SNR in dB.
    """
    signal_power = torch.mean(reference**2)
    noise_power = torch.mean(noise**2)

    if noise_power < 1e-10:
        return float("inf")

    snr = 10 * torch.log10(signal_power / noise_power)
    return snr.item()


def compute_pesq(
    reference: torch.Tensor,
    estimated: torch.Tensor,
    sample_rate: int = 16000,
) -> float | None:
    """Compute PESQ score.

    Args:
        reference: Clean reference signal.
        estimated: Enhanced signal.
        sample_rate: Sample rate (must be 8000 or 16000).

    Returns:
        PESQ score or None if pesq library is not installed.
    """
    try:
        from pesq import pesq as pesq_fn

        ref_np = reference.flatten().numpy()
        est_np = estimated.flatten().numpy()

        mode = "wb" if sample_rate == 16000 else "nb"
        return pesq_fn(sample_rate, ref_np, est_np, mode)
    except ImportError:
        return None


def compute_stoi(
    reference: torch.Tensor,
    estimated: torch.Tensor,
    sample_rate: int = 16000,
) -> float | None:
    """Compute STOI score.

    Args:
        reference: Clean reference signal.
        estimated: Enhanced signal.
        sample_rate: Sample rate.

    Returns:
        STOI score (0 to 1) or None if pystoi is not installed.
    """
    try:
        from pystoi import stoi as stoi_fn

        ref_np = reference.flatten().numpy()
        est_np = estimated.flatten().numpy()

        return stoi_fn(ref_np, est_np, sample_rate, extended=False)
    except ImportError:
        return None


def evaluate(
    reference: torch.Tensor,
    estimated: torch.Tensor,
    sample_rate: int = 16000,
) -> QualityMetrics:
    """Run all available quality metrics.

    Args:
        reference: Clean reference signal.
        estimated: Enhanced signal.
        sample_rate: Sample rate of both signals.

    Returns:
        QualityMetrics with all computed scores.
    """
    return QualityMetrics(
        pesq=compute_pesq(reference, estimated, sample_rate),
        stoi=compute_stoi(reference, estimated, sample_rate),
        si_sdr=compute_si_sdr(reference, estimated),
        snr=compute_snr(reference, estimated - reference),
    )
