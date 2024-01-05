import pyaudio
import numpy as np
import time
from pydub import AudioSegment
import threading

# Define the number of voices and the pitch offset in semitones from the original voice
num_voices = 12  # Number of voices to generate
pitch_shift = 12  # Pitch shift for all voices (in semitones)

# Parameters for the audio processing
CHUNK = 128  # Number of frames per buffer (further reduced for lower latency)
FORMAT = pyaudio.paInt16  # pydub works with 16-bit audio
CHANNELS = 1
RATE = 44100  # Sample rate

# Function to generate the pitch-shifted audio signal for a single voice
def pitch_shift_audio(audio, sample_rate, pitch_shift_value):
    sound = AudioSegment(
        data=audio.tobytes(),
        sample_width=audio.dtype.itemsize,
        frame_rate=sample_rate,
        channels=1
    )
    shifted_sound = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * (2 ** (pitch_shift_value / 12.0)))
    })
    return np.array(shifted_sound.get_array_of_samples(), dtype=np.int16)

# Function to generate the pitch-shifted audio signal for a single voice with reduced gain
def generate_voice(original_signal, sample_rate, pitch_shift_value, gain_factor=0.5):
    shifted_signal = pitch_shift_audio(original_signal, sample_rate, pitch_shift_value)
    processed_data = shifted_signal[:len(original_signal)]
    processed_data = (processed_data * gain_factor).astype(np.int16)  # Applying gain control
    return processed_data

# Function to process the audio stream
def audio_callback(in_data, frame_count, time_info, status):
    audio_data = np.frombuffer(in_data, dtype=np.int16)
    
    # Process the audio for different voices with pitch shift and reduced gain
    processed_data = np.zeros(len(audio_data), dtype=np.int16)
    for i in range(num_voices):
        processed_data += generate_voice(audio_data, RATE, pitch_shift)
    
    return processed_data.tobytes(), pyaudio.paContinue

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

print("Voices with pitch shift effect running...")

# Start stream in a separate thread
stream_thread = threading.Thread(target=stream.start_stream)
stream_thread.start()

# Keep the effect running
try:
    while stream.is_active():
        time.sleep(0.01)
except KeyboardInterrupt:
    pass

# Stop stream and terminate audio
stream.stop_stream()
stream.close()
audio.terminate()
