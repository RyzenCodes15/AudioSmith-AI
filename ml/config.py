"""
AudioSmith AI — ML Pipeline Configuration.

Settings specific to the ML pipeline (model paths, sample rates, etc.).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


@dataclass
class MLConfig:
    """ML pipeline configuration.

    Separated from the backend settings to allow the ML pipeline
    to be used independently (e.g., for training, evaluation scripts).
    """

    # ── Model ────────────────────────────────────────────────────────
    model_name: str = "deepfilternet"
    model_checkpoint_path: str = ""
    device: str = "cpu"

    # ── Audio ────────────────────────────────────────────────────────
    sample_rate: int = 48000
    max_duration_seconds: int = 300
    supported_formats: list[str] = field(
        default_factory=lambda: ["wav", "mp3", "flac", "ogg", "m4a"]
    )

    # ── Paths ────────────────────────────────────────────────────────
    data_dir: Path = Path("data")
    checkpoints_dir: Path = Path("checkpoints")
    outputs_dir: Path = Path("outputs")

    # ── Training ─────────────────────────────────────────────────────
    batch_size: int = 16
    learning_rate: float = 1e-4
    num_epochs: int = 100
    num_workers: int = 4

    # ── Evaluation ───────────────────────────────────────────────────
    eval_sample_rate: int = 16000  # VoiceBank-DEMAND uses 16kHz


def get_ml_config(**overrides) -> MLConfig:
    """Create an ML config with optional overrides."""
    return MLConfig(**overrides)
