import pyaudio
import numpy as np
import time

# Define the harmonies (intervals) in semitones from the original voice
harmony_intervals = [4, 7,0]  # You can modify this list for different harmonies

# Parameters for the audio processing
CHUNK = 512  # Number of frames per buffer
FORMAT = pyaudio.paFloat32
CHANNELS = 2
RATE = 44100  # Sample rate

# Function to generate the harmonized audio signal
def generate_harmony(frames, original_signal):
    processed_data = original_signal.copy()
    for interval in harmony_intervals:
        harmony_signal = np.roll(original_signal, interval * int(RATE / 440))
        processed_data += harmony_signal[:len(original_signal)]
    return frames + processed_data * 0.1  # Applying gain control (adjust as needed)

# Function to process the audio stream
def audio_callback(in_data, frame_count, time_info, status):
    audio_data = np.frombuffer(in_data, dtype=np.float32)
    
    # Process the audio for harmony effect
    processed_data = generate_harmony(audio_data, audio_data)
    
    return processed_data, pyaudio.paContinue

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open stream
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK,
                    stream_callback=audio_callback)

print("Harmony effect running...")

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
