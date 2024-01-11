def generate_pitch_array(num_voices, pitch_offset):
    pitch_array = []
    if num_voices % 2 == 0:
        start = -((num_voices // 2) - 1) * pitch_offset
    else:
        start = -((num_voices - 1) // 2) * pitch_offset

    for i in range(num_voices):
        pitch_array.append(start + i * pitch_offset)

    return pitch_array


# Example usage:
""" num_voices = 3
pitch_offset = 6
result = generate_pitch_array(num_voices, pitch_offset)
print(result) """
for num_voices in range(1, 13):
    for pitch_offset in range(1, 13):
        result = generate_pitch_array(num_voices, pitch_offset)
        print(f"Num Voices: {num_voices}, Pitch Offset: {pitch_offset}, Result: {result}")

##################################################
import pyaudio
import numpy as np

# Constants
CHUNK = 218
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
PITCH_SHIFT = 1.0 # Change this value to alter the pitch (1.0 = original pitch)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Create PyAudio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

print("Pitch-shifting live audio. Press Ctrl+C to stop.")

try:
    while True:
        # Read audio data from the stream
        data = stream.read(CHUNK)
        signal = np.frombuffer(data, dtype=np.float32)

        # Shift the pitch using a time-stretching method
        shifted_signal = np.interp(np.linspace(0, len(signal) - 1, int(len(signal) * PITCH_SHIFT)), np.arange(0, len(signal)), signal)

        # Adjust the length of the signal to match the original length
        if len(shifted_signal) != len(signal):
            if len(shifted_signal) > len(signal):
                shifted_signal = shifted_signal[:len(signal)]
            else:
                shifted_signal = np.append(shifted_signal, [0] * (len(signal) - len(shifted_signal)))

        # Convert shifted signal back to bytes
        processed_audio = shifted_signal.astype(np.float32).tobytes()

        # Play the processed audio
        stream.write(processed_audio)

except KeyboardInterrupt:
    print("Stopping the live audio pitch-shifting.")
    stream.stop_stream()
    stream.close()
    p.terminate()
