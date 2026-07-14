import numpy as np
import soundfile as sf
import os

os.makedirs('test_audio', exist_ok=True)

# Generate a 2-second 440Hz sine wave + noise
sample_rate = 48000
t = np.linspace(0, 2, 2 * sample_rate, False)
audio = np.sin(440 * 2 * np.pi * t) + np.random.normal(0, 0.1, len(t))
audio = audio * 0.5 # Scale down

sf.write('test_audio/sample.wav', audio, sample_rate, format='WAV', subtype='PCM_16')
sf.write('test_audio/sample.mp3', audio, sample_rate, format='MP3')
sf.write('test_audio/sample.flac', audio, sample_rate, format='FLAC', subtype='PCM_16')
