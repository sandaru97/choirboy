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

def generate_time_shifts(num_voices, max_time_shift):
    return [np.random.uniform(-max_time_shift, max_time_shift) for _ in range(num_voices)]

def generate_pitch_variations(num_voices, max_pitch_variation):
    return [np.random.uniform(-max_pitch_variation, max_pitch_variation) for _ in range(num_voices)]

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

# Ask user for pitch offset and number of voices
pitch_offset = get_valid_pitch_offset()
num_voices = get_valid_num_voices()

max_time_shift = 0.05  # 20 milliseconds
max_pitch_variation = 1  # Adjust based on your preference

pitch_shifts = generate_pitch_array(num_voices, pitch_offset)
time_shifts = generate_time_shifts(num_voices, max_time_shift)
pitch_variations = generate_pitch_variations(num_voices, max_pitch_variation)

def apply_choir_effect_live_wav(input_file, pitch_shifts, time_shifts, pitch_variations):
    sample_rate, audio_data_int = wavfile.read(input_file)
    audio_data_float = audio_data_int.astype(np.float32) / 32767.0  # Convert to float and normalize

    while True:
        mixed_audio_data = np.zeros_like(audio_data_float)

        for shift, time_shift, pitch_variation in zip(pitch_shifts, time_shifts, pitch_variations):
            # Apply pitch shift
            shifted_audio = np.roll(audio_data_float, int(shift * len(audio_data_float) / 1200))

            # Apply pitch variation
            pitch_variation_samples = int(pitch_variation * sample_rate)
            shifted_audio = np.roll(shifted_audio, pitch_variation_samples)

            # Apply time shift
            time_shift_samples = int(time_shift * sample_rate)
            shifted_audio = np.roll(shifted_audio, time_shift_samples)

            mixed_audio_data += shifted_audio / len(pitch_shifts)

        # Normalize mixed audio data
        mixed_audio_data /= np.max(np.abs(mixed_audio_data)) / 0.9
        mixed_audio_data = np.clip(mixed_audio_data, -1.0, 1.0)

        # Add breath sounds
        breath_chance = 0.02  # 2% chance of breath sound
        if np.random.rand() < breath_chance:
            breath_length = len(mixed_audio_data)
            breath_sound = np.random.normal(0, 0.01, breath_length)
            mixed_audio_data += breath_sound.reshape(-1, 1)

        sd.play(mixed_audio_data, sample_rate)
        sd.wait()

        time.sleep(len(audio_data_float) / sample_rate)

# Example usage:
input_file_wav = "choirboyaudio.wav"
apply_choir_effect_live_wav(input_file_wav, pitch_shifts, time_shifts, pitch_variations)
