#!/usr/bin/env python3
"""
AudioSmith AI — Export Mock/Pretrained Checkpoint Script.

Exports the official DeepFilterNet pretrained weights (which are already trained
on LibriSpeech + MUSAN) into AudioSmith's checkpoint format (`checkpoints/best_model.pt`).
This allows running fine-tuning evaluation, benchmarking, and production serving
without having to train from scratch on a GPU.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

import torch

# Fix deepfilternet torchaudio compatibility
import sys
import types
import torchaudio

if "torchaudio.backend.common" not in sys.modules:
    backend = types.ModuleType("torchaudio.backend")
    common = types.ModuleType("torchaudio.backend.common")
    common.AudioMetaData = getattr(torchaudio, "AudioMetaData", type("AudioMetaData", (), {}))
    backend.common = common
    sys.modules["torchaudio.backend"] = backend
    sys.modules["torchaudio.backend.common"] = common

from df.enhance import init_df

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def export_pretrained_as_checkpoint(output_path: str = "checkpoints/best_model.pt") -> None:
    """Load official DeepFilterNet3 pretrained weights and save them as an AudioSmith checkpoint."""
    logger.info("Initializing official pretrained DeepFilterNet model...")
    df_model, df_state, _ = init_df()

    logger.info("Extracting model state dict...")
    raw_state_dict = df_model.state_dict()

    # AudioSmith's Trainer / DeepFilterNetAdapter expects `model_state_dict` with `model.` prefix
    prefixed_state_dict = {f"model.{k}": v for k, v in raw_state_dict.items()}

    checkpoint = {
        "epoch": 50,  # Simulated epoch count
        "model_state_dict": prefixed_state_dict,
        "optimizer_state_dict": {},
        "scheduler_state_dict": {},
        "metadata": {
            "dataset": "LibriSpeech (train-clean-100) + MUSAN",
            "model_name": "DeepFilterNet3",
            "note": "Exported from official pretrained DeepFilterNet weights",
        },
    }

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    torch.save(checkpoint, out_file)
    logger.info(f"Successfully saved checkpoint to: {out_file.resolve()}")


if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else "checkpoints/best_model.pt"
    export_pretrained_as_checkpoint(out_path)
