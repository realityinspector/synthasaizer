
import json
import numpy as np
import soundfile as sf
from scipy.signal import find_peaks, welch

def load_audio_fingerprints(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def read_audio_file(filename):
    data, sample_rate = sf.read(filename)
    return data, sample_rate

def find_click_tracks(audio_data, threshold=0.5):
    peaks, _ = find_peaks(np.abs(audio_data), height=threshold)
    return peaks

def extract_segment_features(audio_data, start, end, sample_rate):
    segment = audio_data[start:end]
    freqs, power = welch(segment, fs=sample_rate, nperseg=len(segment))
    dominant_freq = freqs[np.argmax(power)]
    amplitude = np.sqrt(np.max(power))
    
    # New Feature Extraction: Duration and Wave Type
    duration = (end - start) / sample_rate
    wave_type = identify_wave_type(segment)  # This function needs to be implemented

    return dominant_freq, amplitude, duration, wave_type

def identify_wave_type(segment):
    # Implement a method to identify the wave type (sine, square, triangle, etc.)
    # This could involve analyzing the shape of the waveform or using machine learning techniques
    # Placeholder for now
    return 'sine'

def find_closest_fingerprint(features, fingerprints):
    closest_token = None
    min_diff = np.inf

    for fp in fingerprints:
        # Updated to match the new features (frequency, amplitude, duration, wave type)
        freq_diff = np.abs(features[0] - fp['frequency'])
        amp_diff = np.abs(features[1] - fp['amplitude'])
        dur_diff = np.abs(features[2] - fp['duration'])
        wave_type_diff = 1 if features[3] != fp['wave_type'] else 0
        
        total_diff = freq_diff + amp_diff + dur_diff + wave_type_diff
        if total_diff < min_diff:
            min_diff = total_diff
            closest_token = fp['token']

    return closest_token

# Example usage
if __name__ == "__main__":
    # Example process of decoding
    fingerprints = load_audio_fingerprints('audio_fingerprints.json')
    audio_data, sample_rate = read_audio_file('encoded_phrase.wav')
    click_tracks = find_click_tracks(audio_data)
    tokens = []

    start_index = 0
    for click_index in click_tracks:
        features = extract_segment_features(audio_data, start_index, click_index, sample_rate)
        token = find_closest_fingerprint(features, fingerprints)
        tokens.append(token)
        start_index = click_index + 1

    decoded_phrase = ' '.join(tokens)
    print(decoded_phrase)
