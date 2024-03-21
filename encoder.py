# encoder.py

import json
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import os

def generate_tone(frequency, amplitude, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(frequency * t * 2 * np.pi)
    return tone * amplitude

def generate_silence(duration=0.1, sample_rate=44100):
    return np.zeros(int(sample_rate * duration))

def encode_phrase(phrase, fingerprints_files, encoded_file, encoded_text_file, encoded_fingerprints_file):
    tokens = phrase.split()
    audio_signal = np.array([])
    encoded_fingerprints = {}

    placeholder_token = {'token': '<MISSING>', 'frequency': 100, 'amplitude': 0.5, 'duration': 0.1}

    fingerprint_dict = {}
    for fingerprints_file in fingerprints_files:
        with open(fingerprints_file, 'r') as file:
            fingerprints = json.load(file)
            fingerprint_dict.update({fp['token']: fp for fp in fingerprints})

    for token in tokens:
        if token in fingerprint_dict:
            fp = fingerprint_dict[token]
            encoded_fingerprints[token] = fp
        else:
            encoded_fingerprints[token] = placeholder_token

    for token in tokens:
        fp = encoded_fingerprints[token]
        tone = generate_tone(fp['frequency'], fp['amplitude'], fp['duration'])
        audio_signal = np.concatenate((audio_signal, tone))
        silence = generate_silence()
        audio_signal = np.concatenate((audio_signal, silence))

    sf.write(encoded_file, audio_signal, 44100)

    # Save the encoded text
    with open(encoded_text_file, 'w') as file:
        file.write(phrase)

    # Save the encoded fingerprints
    with open(encoded_fingerprints_file, 'w') as file:
        json.dump(encoded_fingerprints, file)

    plt.figure(figsize=(10, 4))
    plt.plot(audio_signal)
    plt.title('Encoded Waveform')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.tight_layout()
    plt.savefig(f'{os.path.splitext(encoded_file)[0]}.png')
    plt.close()