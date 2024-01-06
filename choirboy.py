import pyaudio
import numpy as np
import time

# Parameters for the audio processing
CHUNK = 1024  # Smaller buffer size for reduced latency
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100  # Standard sample rate

# Function to generate the harmonized audio signal with multiple harmonies
def generate_multiple_harmonies(original_signal, num_voices, pitch_offset):
    pitch_offsets = np.arange(1, num_voices + 1) * pitch_offset * (-1) ** np.arange(1, num_voices + 1)
    processed_data = np.zeros_like(original_signal)
    
    for voice_idx in range(num_voices):
        intervals = pitch_offsets[:voice_idx + 1]
        for interval in intervals:
            shifted_signal = np.roll(original_signal, int(interval * RATE / 440))
            processed_data += shifted_signal[:len(original_signal)]

    return processed_data * 0.1  # Adjust gain for optimal volume (may require testing)

# Function to process the audio stream
def audio_callback(in_data, frame_count, time_info, status):
    audio_data = np.frombuffer(in_data, dtype=np.float32)
    
    # Define the number of voices and a single pitch offset value for generating array of pitch offsets
    num_voices = 2  # You can modify this for different numbers of voices
    pitch_offset = 6  # You can modify this for different pitch offset
    
    # Process the audio for multiple harmony effect
    processed_data = generate_multiple_harmonies(audio_data, num_voices, pitch_offset)
    
    return processed_data.tobytes(), pyaudio.paContinue

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open stream with reduced buffer size and standard sample rate
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK,  # Smaller buffer size for reduced latency
                    stream_callback=audio_callback)

print("Harmony Effect Running with Reduced Lag...")

# Start stream
stream.start_stream()

# Keep the effect running
try:
    while stream.is_active():
        time.sleep(0.1)
except KeyboardInterrupt:
    pass

# Stop stream
stream.stop_stream()
stream.close()
audio.terminate()
