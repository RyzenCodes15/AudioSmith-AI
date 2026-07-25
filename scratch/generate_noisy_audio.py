import os
import numpy as np
import librosa
import soundfile as sf

def generate_noisy_audio(output_path="test_audio/extreme_noise_test.wav"):
    print("Downloading sample speech (LibriSpeech snippet)...")
    # librosa.ex('libri1') downloads a short clean speech file from librosa's datasets
    audio_path = librosa.ex('libri1')
    
    print(f"Loading {audio_path}...")
    # Load audio at native 48kHz for DeepFilterNet optimal performance (or 16kHz)
    # DeepFilterNet natively expects 48kHz.
    target_sr = 48000
    clean_audio, sr = librosa.load(audio_path, sr=target_sr)
    
    print("Generating extreme background noise...")
    # Generate pink noise / uniform noise
    noise = np.random.normal(0, 0.5, len(clean_audio))
    
    # Mix audio (extreme noise: SNR ~ -10dB to 0dB)
    # Clean audio typical amplitude is around 0.1 to 0.3
    # Let's boost the noise heavily.
    noisy_audio = clean_audio + (noise * 0.8)
    
    # Peak normalize to prevent clipping
    max_val = np.max(np.abs(noisy_audio))
    if max_val > 0:
        noisy_audio = noisy_audio / max_val * 0.95
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sf.write(output_path, noisy_audio, target_sr, format='WAV', subtype='PCM_16')
    print(f"Successfully generated extreme noisy audio at: {output_path}")
    print(f"Length: {len(noisy_audio)/target_sr:.2f} seconds | Sample Rate: {target_sr} Hz")

if __name__ == "__main__":
    generate_noisy_audio()
