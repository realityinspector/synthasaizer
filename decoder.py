#decoder.py
import json
import numpy as np
import soundfile as sf
from scipy.signal import find_peaks, welch
import matplotlib.pyplot as plt
import os


def load_audio_fingerprints(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def read_audio_file(filename):
    data, sample_rate = sf.read(filename)
    return data, sample_rate

def find_tone_segments(audio_data, threshold=0.01, min_duration=0.05, sample_rate=44100):
    peaks, _ = find_peaks(np.abs(audio_data), height=threshold)
    segments = []
    start_index = 0

    for i in range(len(peaks)):
        if i == len(peaks) - 1 or peaks[i+1] - peaks[i] > min_duration * sample_rate:
            segments.append((start_index, peaks[i]))
            start_index = peaks[i] + 1

    return segments

def extract_segment_features(audio_data, start, end, sample_rate):
    segment = audio_data[start:end]
    freqs, power = welch(segment, fs=sample_rate, nperseg=len(segment))
    dominant_freq = freqs[np.argmax(power)]
    amplitude = np.sqrt(np.max(power))
    return dominant_freq, amplitude

def find_closest_fingerprint(features, fingerprints):
    closest_token = None
    min_diff = np.inf

    for fp in fingerprints:
        freq_diff = np.abs(features[0] - fp['frequency'])
        amp_diff = np.abs(features[1] - fp['amplitude'])
        total_diff = freq_diff + amp_diff

        if total_diff < min_diff:
            min_diff = total_diff
            closest_token = fp['token']

    return closest_token

def decode_phrase(encoded_file, fingerprints_file, decoded_file, decoded_text_file, decoded_fingerprints_file):
    fingerprints = load_audio_fingerprints(fingerprints_file)
    audio_data, sample_rate = read_audio_file(encoded_file)
    segments = find_tone_segments(audio_data)
    tokens = []

    for start, end in segments:
        features = extract_segment_features(audio_data, start, end, sample_rate)
        token = find_closest_fingerprint(features, fingerprints)
        tokens.append(token)

    decoded_phrase = ' '.join(tokens)

    # Save the decoded audio
    sf.write(decoded_file, audio_data, sample_rate)

    # Save the decoded text
    with open(decoded_text_file, 'w') as file:
        file.write(decoded_phrase)

    # Save the decoded fingerprints
    decoded_fingerprints = [fp for fp in fingerprints if fp['token'] in tokens]
    with open(decoded_fingerprints_file, 'w') as file:
        json.dump(decoded_fingerprints, file)

    plt.figure(figsize=(10, 4))
    plt.plot(audio_data)
    plt.title('Decoded Waveform')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.tight_layout()
    plt.savefig(f'{os.path.splitext(decoded_file)[0]}.png')
    plt.close()

    return decoded_phrase