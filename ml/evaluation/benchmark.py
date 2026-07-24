"""
AudioSmith AI — VoiceBank-DEMAND Benchmark Runner.

Evaluates speech enhancement models on the standard
VoiceBank-DEMAND test set.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from ml.evaluation.metrics import QualityMetrics, evaluate
from ml.models.base import BaseSpeechEnhancer
from ml.datasets.dataset import ValidationDataset
import torch

logger = logging.getLogger(__name__)


@dataclass
class BenchmarkResult:
    """Aggregated benchmark results."""

    model_name: str
    num_samples: int
    avg_pesq: float | None
    avg_stoi: float | None
    avg_si_sdr: float | None
    avg_snr: float | None

    def __repr__(self) -> str:
        lines = [
            f"Benchmark Results — {self.model_name}",
            f"  Samples: {self.num_samples}",
            f"  PESQ:    {self.avg_pesq:.3f}" if self.avg_pesq else "  PESQ:    N/A",
            f"  STOI:    {self.avg_stoi:.3f}" if self.avg_stoi else "  STOI:    N/A",
            f"  SI-SDR:  {self.avg_si_sdr:.2f} dB" if self.avg_si_sdr else "  SI-SDR:  N/A",
            f"  SNR:     {self.avg_snr:.2f} dB" if self.avg_snr else "  SNR:     N/A",
        ]
        return "\n".join(lines)


class BenchmarkRunner:
    """Runs evaluation benchmarks on speech enhancement models.

    Evaluates models against the VoiceBank-DEMAND test set and
    computes aggregated quality metrics.
    """

    def __init__(
        self,
        model: BaseSpeechEnhancer,
        dataset_path: Path | str,
        sample_rate: int = 16000,
    ) -> None:
        self._model = model
        self._dataset_path = Path(dataset_path)
        self._sample_rate = sample_rate

    def run(self) -> BenchmarkResult:
        """Run the benchmark evaluation.

        Returns:
            Aggregated benchmark results.
        """
        # 1. Load VoiceBank-DEMAND test set
        clean_dir = self._dataset_path / "clean_testset_wav"
        noisy_dir = self._dataset_path / "noisy_testset_wav"
        
        dataset = ValidationDataset(
            clean_dir=str(clean_dir),
            noisy_dir=str(noisy_dir),
            sample_rate=self._model.get_sample_rate(),
            duration=3.0 # Or evaluate on full length, but for now 3.0 to match training chunks
        )
        
        if len(dataset) == 0:
            raise RuntimeError(f"No audio files found in {self._dataset_path}")

        metrics_sum = {"pesq": 0.0, "stoi": 0.0, "si_sdr": 0.0, "snr": 0.0}
        counts = {"pesq": 0, "stoi": 0, "si_sdr": 0, "snr": 0}
        
        for i in range(len(dataset)):
            noisy, clean = dataset[i]
            
            # Add batch dimension for inference
            noisy_batch = noisy.unsqueeze(0)
            
            with torch.no_grad():
                enhanced_batch = self._model.enhance(noisy_batch)
                
            enhanced = enhanced_batch.squeeze(0)
            
            # Evaluate using resampler in evaluate function if needed
            res = evaluate(clean, enhanced, sample_rate=self._model.get_sample_rate())
            
            for k in metrics_sum.keys():
                val = getattr(res, k, None)
                if val is not None:
                    metrics_sum[k] += val
                    counts[k] += 1
                    
        return BenchmarkResult(
            model_name=self._model.get_model_name(),
            num_samples=len(dataset),
            avg_pesq=metrics_sum["pesq"] / counts["pesq"] if counts["pesq"] > 0 else None,
            avg_stoi=metrics_sum["stoi"] / counts["stoi"] if counts["stoi"] > 0 else None,
            avg_si_sdr=metrics_sum["si_sdr"] / counts["si_sdr"] if counts["si_sdr"] > 0 else None,
            avg_snr=metrics_sum["snr"] / counts["snr"] if counts["snr"] > 0 else None,
        )
