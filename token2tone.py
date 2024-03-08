
import json
import numpy as np

def generate_audio_fingerprint(token, index, total_tokens):
    '''
    Generate a unique audio fingerprint for each token.

    Args:
    - token: The token for which to generate the fingerprint.
    - index: The index of the token in the list.
    - total_tokens: The total number of tokens to be processed.

    Returns:
    - A dictionary containing the token's audio fingerprint.
    '''
    # Define base audio properties
    base_frequency = 300
    max_frequency = 3000
    frequency_step = (max_frequency - base_frequency) / total_tokens

    # Assign unique frequency to each token
    frequency = base_frequency + frequency_step * index

    # Variable amplitude and duration
    amplitude = 0.5 + (index % 3) * 0.25  # Varying amplitude (0.5, 0.75, 1.0)
    duration = 0.1 + (index % 4) * 0.05   # Varying duration (0.1, 0.15, 0.2, 0.25)

    # Wave type variation
    wave_types = ['sine', 'square', 'triangle', 'sawtooth']
    wave_type = wave_types[index % len(wave_types)]

    return {
        'token': token['string'],
        'id': token['id'],
        'frequency': frequency,
        'amplitude': amplitude,
        'wave_type': wave_type,
        'duration': duration
    }

# Example usage
if __name__ == "__main__":
    # Generate fingerprints for a set of example tokens
    example_tokens = [{'string': 'token1', 'id': 1}, {'string': 'token2', 'id': 2}]
    fingerprints = [generate_audio_fingerprint(token, i, len(example_tokens)) for i, token in enumerate(example_tokens)]
    print(fingerprints)
