import sounddevice as sd
import numpy as np
from scipy.io import wavfile
import time

def generate_pitch_array(num_voices, pitch_offset):
    pitch_array = []
    if num_voices % 2 == 0:
        start = -((num_voices // 2) - 1) * pitch_offset
    else:
        start = -((num_voices - 1) // 2) * pitch_offset

    for i in range(num_voices):
        pitch_array.append(start + i * pitch_offset)

    return pitch_array

def get_valid_pitch_offset():
    while True:
        pitch_offset = float(input("Enter the pitch offset (1 to 12): "))
        if 1 <= pitch_offset <= 12:
            return pitch_offset
        else:
            print("Invalid pitch offset. Please enter a value between 1 and 12.")

def get_valid_num_voices():
    while True:
        num_voices = int(input("Enter the number of voices (1 to 12): "))
        if 1 <= num_voices <= 12:
            return num_voices
        else:
            print("Invalid number of voices. Please enter a value between 1 and 12.")

def apply_choir_effect_live_stereo(input_file, pitch_offset, num_voices):
    sample_rate, audio_data_int = wavfile.read(input_file)
    audio_data_float = audio_data_int.astype(np.float32) / 32767.0  # Convert to float and normalize

    pitch_shifts = generate_pitch_array(num_voices, pitch_offset)

    while True:
        mixed_audio_data = np.zeros((len(audio_data_float), 2), dtype=np.float32)

        for i, pitch_shift in enumerate(pitch_shifts):
            # Apply pitch shift
            shifted_audio = np.roll(audio_data_float, int(pitch_shift * len(audio_data_float) / 1200), axis=0)

            # Take only the first column of shifted_audio (for stereo)
            shifted_audio = shifted_audio[:, 0]

            # Distribute voices evenly between left and right channels
            if i % 2 == 0:
                mixed_audio_data[:, 0] += shifted_audio / (num_voices // 2)
            else:
                mixed_audio_data[:, 1] += shifted_audio / (num_voices // 2)

        # Normalize mixed audio data
        mixed_audio_data /= np.max(np.abs(mixed_audio_data)) / 0.9
        mixed_audio_data = np.clip(mixed_audio_data, -1.0, 1.0)

        sd.play(mixed_audio_data, sample_rate, blocking=True)

        time.sleep(len(audio_data_float) / sample_rate)

# Example usage:
pitch_offset = get_valid_pitch_offset()
num_voices = get_valid_num_voices()

input_file_wav = "choirboyaudio0.wav"
apply_choir_effect_live_stereo(input_file_wav, pitch_offset, num_voices)
