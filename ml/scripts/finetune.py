import os
import yaml
import logging
from pathlib import Path
from torch.utils.data import DataLoader

# Fix deepfilternet torchaudio compatibility
import sys
import types
import torchaudio
if "torchaudio.backend.common" not in sys.modules:
    backend = types.ModuleType('torchaudio.backend')
    common = types.ModuleType('torchaudio.backend.common')
    common.AudioMetaData = getattr(torchaudio, 'AudioMetaData', type('AudioMetaData', (), {}))
    backend.common = common
    sys.modules['torchaudio.backend'] = backend
    sys.modules['torchaudio.backend.common'] = common

from df.enhance import init_df

from ml.datasets.dataset import NoisyCleanDataset, ValidationDataset
from ml.trainers.wrapper import FineTuneWrapper
from ml.trainers.trainer import Trainer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def main():
    config_path = Path("ml/configs/train_config.yaml")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        
    logger.info("Initializing datasets...")
    train_dataset = NoisyCleanDataset(
        clean_dir=config["datasets"]["clean_dir"],
        noise_dir=config["datasets"]["noise_dir"],
        sample_rate=config["datasets"]["sample_rate"],
        duration=config["datasets"]["duration"],
        snr_range=config["datasets"]["snr_range"],
        seed=config["seed"]
    )
    
    val_dataset = ValidationDataset(
        clean_dir=config["datasets"]["eval_clean_dir"],
        noisy_dir=config["datasets"]["eval_noisy_dir"],
        sample_rate=config["datasets"]["sample_rate"],
        duration=config["datasets"]["duration"]
    )
    
    train_loader = DataLoader(
        train_dataset, 
        batch_size=config["training"]["batch_size"], 
        shuffle=True, 
        num_workers=config["training"]["num_workers"],
        drop_last=True
    )
    
    val_loader = DataLoader(
        val_dataset, 
        batch_size=config["training"]["batch_size"], 
        shuffle=False, 
        num_workers=config["training"]["num_workers"]
    )
    
    logger.info("Initializing DeepFilterNet model...")
    # Load the official pretrained DeepFilterNet model to start fine-tuning from
    df_model, df_state, _ = init_df()
    
    logger.info("Wrapping model for fine-tuning...")
    wrapper = FineTuneWrapper(df_model, sample_rate=config["datasets"]["sample_rate"])
    
    logger.info("Starting trainer...")
    trainer = Trainer(
        model=wrapper,
        train_loader=train_loader,
        val_loader=val_loader,
        config=config
    )
    
    trainer.train()
    logger.info("Training complete!")

if __name__ == "__main__":
    main()
