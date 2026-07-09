"""
AudioSmith AI — Evaluation Script.

Entry point for evaluating models against the VoiceBank-DEMAND benchmark.
"""

from __future__ import annotations

import argparse
import logging

from ml.evaluation.benchmark import BenchmarkRunner
from ml.models.registry import get_registry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate AudioSmith models.")
    parser.add_argument("--model", type=str, required=True, help="Model name (e.g., deepfilternet)")
    parser.add_argument("--checkpoint", type=str, help="Path to model checkpoint")
    parser.add_argument("--dataset-dir", type=str, default="data/VoiceBank-DEMAND", help="Path to benchmark dataset")
    args = parser.parse_args()

    logger.info("Evaluating model: %s", args.model)
    registry = get_registry()
    model = registry.create(args.model)
    model.load(args.checkpoint)
    
    runner = BenchmarkRunner(model=model, dataset_path=args.dataset_dir)
    result = runner.run()
    print(result)


if __name__ == "__main__":
    main()
