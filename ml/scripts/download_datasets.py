"""
AudioSmith AI — Dataset Downloader.

Automates the downloading and extraction of training and evaluation datasets:
- LibriSpeech (clean)
- MUSAN (noise)
- VoiceBank-DEMAND (evaluation)
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

# Future: import requests, tarfile, zipfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_librispeech(output_dir: Path) -> None:
    """Download LibriSpeech dataset."""
    logger.info("Downloading LibriSpeech to %s...", output_dir)
    raise NotImplementedError("LibriSpeech download not implemented.")


def download_musan(output_dir: Path) -> None:
    """Download MUSAN dataset."""
    logger.info("Downloading MUSAN to %s...", output_dir)
    raise NotImplementedError("MUSAN download not implemented.")


def download_voicebank_demand(output_dir: Path) -> None:
    """Download VoiceBank-DEMAND benchmark dataset."""
    logger.info("Downloading VoiceBank-DEMAND to %s...", output_dir)
    raise NotImplementedError("VoiceBank-DEMAND download not implemented.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Download AudioSmith ML datasets.")
    parser.add_argument("--output-dir", type=Path, default=Path("data"))
    parser.add_argument("--dataset", choices=["all", "librispeech", "musan", "voicebank-demand"], default="all")

    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    if args.dataset in ("all", "librispeech"):
        download_librispeech(args.output_dir)
    if args.dataset in ("all", "musan"):
        download_musan(args.output_dir)
    if args.dataset in ("all", "voicebank-demand"):
        download_voicebank_demand(args.output_dir)


if __name__ == "__main__":
    main()
