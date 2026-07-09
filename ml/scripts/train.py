"""
AudioSmith AI — Training Script.

Entry point for training speech enhancement models.
"""

from __future__ import annotations

import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Train AudioSmith models.")
    parser.add_argument("--config", type=str, required=True, help="Path to YAML config file")
    args = parser.parse_args()

    logger.info("Starting training with config: %s", args.config)
    # Future: parse config, instantiate datasets, model, optimizer, loss, and run training loop
    raise NotImplementedError("Training script not implemented.")


if __name__ == "__main__":
    main()
