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
    parser.add_argument("--model", type=str, default="deepfilternet", help="Model name (e.g., deepfilternet)")
    parser.add_argument("--checkpoint", type=str, help="Path to fine-tuned model checkpoint for comparison")
    parser.add_argument("--dataset-dir", type=str, default="data/VoiceBank", help="Path to benchmark dataset")
    args = parser.parse_args()

    registry = get_registry()
    
    logger.info("Evaluating Official model: %s", args.model)
    official_model = registry.create(args.model)
    official_model.load()
    
    runner = BenchmarkRunner(model=official_model, dataset_path=args.dataset_dir)
    official_result = runner.run()
    print(official_result)
    
    if args.checkpoint:
        logger.info("\nEvaluating Fine-tuned model from: %s", args.checkpoint)
        ft_model = registry.create(args.model)
        ft_model.load(args.checkpoint)
        
        ft_runner = BenchmarkRunner(model=ft_model, dataset_path=args.dataset_dir)
        ft_result = ft_runner.run()
        print(ft_result)
        
        print("\n--- Comparison Report ---")
        metrics = ["avg_pesq", "avg_stoi", "avg_si_sdr", "avg_snr"]
        for m in metrics:
            val_off = getattr(official_result, m)
            val_ft = getattr(ft_result, m)
            if val_off is not None and val_ft is not None:
                diff = val_ft - val_off
                symbol = "+" if diff >= 0 else ""
                print(f"{m.upper()}: {val_off:.4f} -> {val_ft:.4f} ({symbol}{diff:.4f})")

if __name__ == "__main__":
    main()
