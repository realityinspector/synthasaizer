#token2tone.py
import numpy as np

def generate_audio_fingerprint(token, index, total_tokens):
    base_frequency = 300
    max_frequency = 3000
    frequency_step = (max_frequency - base_frequency) / total_tokens

    frequency = base_frequency + frequency_step * index
    amplitude = 0.5
    duration = 0.1

    return {
        'token': token['string'],
        'id': token['id'],
        'frequency': frequency,
        'amplitude': amplitude,
        'duration': duration
    }