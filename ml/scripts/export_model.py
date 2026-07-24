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

    import torch
    from df.enhance import init_df
    from ml.trainers.wrapper import FineTuneWrapper

    logger.info("Exporting %s to %s format at %s", args.model, args.format, args.output)
    
    # Load official model
    df_model, _, _ = init_df()
    wrapper = FineTuneWrapper(df_model)
    
    # Load fine-tuned weights
    state_dict = torch.load(args.checkpoint, map_location="cpu")
    
    if "model_state_dict" in state_dict:
        wrapper.load_state_dict(state_dict["model_state_dict"])
    else:
        wrapper.load_state_dict(state_dict)
        
    wrapper.eval()
    
    dummy_input = torch.randn(1, 1, 48000 * 3) # 3 seconds of audio at 48kHz
    
    if args.format == "onnx":
        torch.onnx.export(
            wrapper, 
            dummy_input, 
            args.output,
            export_params=True,
            opset_version=14,
            do_constant_folding=True,
            input_names=['input_audio'],
            output_names=['enhanced_audio'],
            dynamic_axes={'input_audio': {0: 'batch_size', 2: 'sequence_length'},
                          'enhanced_audio': {0: 'batch_size', 2: 'sequence_length'}}
        )
        logger.info(f"Successfully exported to ONNX: {args.output}")
    else:
        raise NotImplementedError(f"Format {args.format} not implemented yet.")


if __name__ == "__main__":
    main()
