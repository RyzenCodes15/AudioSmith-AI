"""
AudioSmith AI — Model Export.

Exports trained PyTorch models to optimized formats (ONNX, TorchScript)
for serving.
"""

from __future__ import annotations

import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export AudioSmith models.")
    parser.add_argument("--model", type=str, required=True)
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("--format", choices=["onnx", "torchscript"], default="torchscript")
    args = parser.parse_args()

    logger.info("Exporting %s to %s format at %s", args.model, args.format, args.output)
    raise NotImplementedError("Model export not implemented.")


if __name__ == "__main__":
    main()
