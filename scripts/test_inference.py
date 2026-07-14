import torch
import torchaudio
import requests
import time
import os

# 1. Generate test audio (3 seconds of noise + tone)
os.makedirs('/tmp/test_audio', exist_ok=True)
sr = 48000
t = torch.linspace(0, 3, 3 * sr)
tone = torch.sin(2 * 3.1415 * 440 * t)
noise = torch.randn(3 * sr) * 0.1
audio = (tone + noise).unsqueeze(0)  # [1, samples]

wav_path = '/tmp/test_audio/test.wav'
torchaudio.save(wav_path, audio, sr)

# Note: since we only have torchaudio easily available, let's just upload the WAV 3 times
# to prove the pipeline works, or use the container's ffmpeg to convert it.
