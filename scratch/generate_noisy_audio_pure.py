import wave
import struct
import random
import os

def create_noisy_audio(input_file, output_file, loop_count=5):
    print(f"Reading base audio from {input_file}...")
    with wave.open(input_file, 'rb') as wav_in:
        params = wav_in.getparams()
        # Read the raw frames (PCM 16-bit)
        frames = wav_in.readframes(params.nframes)
        
    # Unpack bytes into integers (assuming 16-bit mono)
    # The format string 'h' represents a C short (2 bytes)
    # '<' means little-endian, which is standard for WAV files
    num_samples = params.nframes * params.nchannels
    format_str = f"<{num_samples}h"
    samples = list(struct.unpack(format_str, frames))
    
    # Loop the samples to make the file longer
    samples = samples * loop_count
    
    print("Generating extreme background noise and mixing...")
    noisy_samples = []
    
    # Clean audio is typically well within the short int range (-32768 to 32767)
    # We will mix very loud noise.
    max_amp = 32767
    
    for sample in samples:
        # Generate random noise (uniform distribution)
        # 0.8 scale means very loud noise
        noise = random.uniform(-max_amp * 0.8, max_amp * 0.8)
        
        # Mix clean + noise
        mixed = sample + noise
        
        # Hard clipping to prevent overflow
        if mixed > max_amp:
            mixed = max_amp
        elif mixed < -max_amp - 1:
            mixed = -max_amp - 1
            
        noisy_samples.append(int(mixed))
        
    print(f"Writing noisy audio to {output_file}...")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with wave.open(output_file, 'wb') as wav_out:
        # Update params (number of frames is now looped)
        wav_out.setparams((
            params.nchannels, 
            params.sampwidth, 
            params.framerate, 
            len(noisy_samples) // params.nchannels, 
            params.comptype, 
            params.compname
        ))
        
        # Pack back into bytes
        out_format_str = f"<{len(noisy_samples)}h"
        out_frames = struct.pack(out_format_str, *noisy_samples)
        wav_out.writeframes(out_frames)
        
    print(f"Successfully generated extreme noisy audio at: {output_file}")
    
if __name__ == "__main__":
    create_noisy_audio("test.wav", "test_audio/extreme_noise_test.wav", loop_count=5)
