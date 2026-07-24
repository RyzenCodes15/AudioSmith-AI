import os
import time
from pathlib import Path
from typing import Dict, Any

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.cuda.amp import GradScaler, autocast
import mlflow
from torchmetrics.audio import ScaleInvariantSignalDistortionRatio

import logging
logger = logging.getLogger(__name__)

class Trainer:
    """Trainer class for DeepFilterNet fine-tuning pipeline."""
    
    def __init__(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        val_loader: DataLoader,
        config: Dict[str, Any]
    ):
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.config = config
        
        self.device = torch.device(config.get("device", "cpu"))
        self.model.to(self.device)
        
        # Loss function: Negative SI-SDR
        self.criterion = ScaleInvariantSignalDistortionRatio().to(self.device)
        
        # Optimizer and Scheduler
        self.optimizer = optim.AdamW(
            self.model.parameters(), 
            lr=config["training"].get("learning_rate", 1e-4),
            weight_decay=config["training"].get("weight_decay", 1e-2)
        )
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer, mode='min', factor=0.5, patience=5
        )
        
        self.mixed_precision = config["training"].get("mixed_precision", True)
        self.scaler = GradScaler(enabled=self.mixed_precision)
        
        # Paths
        self.checkpoints_dir = Path(config["outputs"]["checkpoints_dir"])
        self.checkpoints_dir.mkdir(parents=True, exist_ok=True)
        
        self.num_epochs = config["training"]["num_epochs"]
        self.early_stopping_patience = config["training"].get("early_stopping_patience", 10)
        
    def _compute_loss(self, preds: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        # Negative SI-SDR (maximize SI-SDR => minimize -SI-SDR)
        return -self.criterion(preds, target)

    def train_epoch(self, epoch: int) -> float:
        self.model.train()
        total_loss = 0.0
        
        for batch_idx, (noisy, clean) in enumerate(self.train_loader):
            noisy, clean = noisy.to(self.device), clean.to(self.device)
            
            self.optimizer.zero_grad()
            
            with autocast(enabled=self.mixed_precision):
                enhanced = self.model(noisy)
                loss = self._compute_loss(enhanced, clean)
                
            self.scaler.scale(loss).backward()
            self.scaler.unscale_(self.optimizer)
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            self.scaler.step(self.optimizer)
            self.scaler.update()
            
            total_loss += loss.item()
            
            if batch_idx % 10 == 0:
                logger.info(f"Epoch [{epoch}/{self.num_epochs}] Batch [{batch_idx}/{len(self.train_loader)}] Loss: {loss.item():.4f}")
                mlflow.log_metric("train_batch_loss", loss.item(), step=epoch * len(self.train_loader) + batch_idx)
                
        return total_loss / len(self.train_loader)

    @torch.no_grad()
    def validate(self, epoch: int) -> float:
        self.model.eval()
        total_loss = 0.0
        
        for noisy, clean in self.val_loader:
            noisy, clean = noisy.to(self.device), clean.to(self.device)
            
            with autocast(enabled=self.mixed_precision):
                enhanced = self.model(noisy)
                loss = self._compute_loss(enhanced, clean)
                
            total_loss += loss.item()
            
        avg_loss = total_loss / len(self.val_loader)
        logger.info(f"Validation Loss: {avg_loss:.4f}")
        mlflow.log_metric("val_loss", avg_loss, step=epoch)
        return avg_loss

    def save_checkpoint(self, epoch: int, is_best: bool = False):
        state = {
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
        }
        
        checkpoint_path = self.checkpoints_dir / f"checkpoint_epoch_{epoch}.pt"
        torch.save(state, checkpoint_path)
        logger.info(f"Saved checkpoint: {checkpoint_path}")
        
        if is_best:
            best_path = self.checkpoints_dir / "best_model.pt"
            torch.save(state, best_path)
            logger.info(f"Saved best model: {best_path}")

    def train(self):
        mlflow.set_tracking_uri(self.config["logging"]["mlflow_tracking_uri"])
        mlflow.set_experiment(self.config["logging"]["experiment_name"])
        
        with mlflow.start_run():
            mlflow.log_params(self.config["training"])
            
            best_val_loss = float('inf')
            patience_counter = 0
            
            for epoch in range(1, self.num_epochs + 1):
                start_time = time.time()
                
                train_loss = self.train_epoch(epoch)
                val_loss = self.validate(epoch)
                
                self.scheduler.step(val_loss)
                
                duration = time.time() - start_time
                logger.info(f"Epoch {epoch} completed in {duration:.2f}s | Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}")
                
                mlflow.log_metric("train_loss_epoch", train_loss, step=epoch)
                mlflow.log_metric("epoch_duration", duration, step=epoch)
                
                is_best = val_loss < best_val_loss
                if is_best:
                    best_val_loss = val_loss
                    patience_counter = 0
                else:
                    patience_counter += 1
                    
                if epoch % self.config["training"].get("checkpoint_interval", 5) == 0 or is_best:
                    self.save_checkpoint(epoch, is_best=is_best)
                    
                if patience_counter >= self.early_stopping_patience:
                    logger.info(f"Early stopping triggered at epoch {epoch}")
                    break
