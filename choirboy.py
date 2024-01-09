def generate_pitch_array(num_voices, pitch_offset):
    pitch_array = []
    offset = -(num_voices // 2) * pitch_offset if num_voices % 2 == 0 else -((num_voices - 1) // 2) * pitch_offset

    for i in range(num_voices):
        pitch_array.append(offset)
        offset += pitch_offset if i < num_voices // 2 else -pitch_offset

    return pitch_array

# Example usage:
num_voices = 3
pitch_offset = 6
result = generate_pitch_array(num_voices, pitch_offset)
print(result)
