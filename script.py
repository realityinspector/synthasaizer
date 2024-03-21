import os
import json
import re
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt
from dtw import dtw

# Global variables
fingerprints_file = 'fingerprints.json'
fingerprints_dict = {}
next_frequency = 10000
frequency_step = 50000
base_amplitude = 0.5
base_duration = 1
tick_duration = 1


def load_fingerprints():
  global fingerprints_dict, next_frequency
  if os.path.exists(fingerprints_file):
    with open(fingerprints_file, 'r') as file:
      fingerprints_dict = json.load(file)
    if fingerprints_dict:
      next_frequency = max(
          fp['frequency']
          for fp in fingerprints_dict.values()) + frequency_step


def save_fingerprints():
  with open(fingerprints_file, 'w') as file:
    json.dump(fingerprints_dict, file, indent=2)


def generate_tone(frequency, amplitude, duration, sample_rate=44100):
  t = np.linspace(0, duration, int(sample_rate * duration), False)
  tone = np.sin(frequency * t * 2 * np.pi)
  return tone * amplitude


def generate_tick(duration=0.05, sample_rate=44100):
  return np.ones(int(sample_rate * duration))


def generate_audio_fingerprint(token):
  global next_frequency
  if token not in fingerprints_dict:
    fingerprints_dict[token] = {
        'token': token,
        'frequency': next_frequency,
        'amplitude': base_amplitude,
        'duration': base_duration
    }
    next_frequency += frequency_step
    save_fingerprints()
  return fingerprints_dict[token]


def encode_phrase(phrase):
  tokens = phrase.split()
  audio_signal = np.array([])
  for token in tokens:
    fp = generate_audio_fingerprint(token)
    tone = generate_tone(fp['frequency'], fp['amplitude'], fp['duration'])
    tick = generate_tick(tick_duration)
    audio_signal = np.concatenate((audio_signal, tone, tick))
  return audio_signal


def decode_phrase(audio_data, sample_rate):
  sos = butter(10, [200, 10000], 'bp', fs=sample_rate, output='sos')
  filtered_audio = sosfilt(sos, audio_data)

  window_size = int(base_duration * sample_rate)
  hop_size = int(tick_duration * sample_rate)
  segments = []
  for i in range(0, len(filtered_audio) - window_size, hop_size):
    segment = filtered_audio[i:i + window_size]
    segments.append(segment)

  tokens = []
  for segment in segments:
    min_distance = float('inf')
    min_token = None
    for fp in fingerprints_dict.values():
      ref_tone = generate_tone(fp['frequency'], fp['amplitude'],
                               fp['duration'], sample_rate)
      distance, _ = dtw(segment, ref_tone, dist=lambda x, y: np.abs(x - y))
      if distance < min_distance:
        min_distance = distance
        min_token = fp['token']
    if min_token is not None:
      tokens.append(min_token)

  return ' '.join(tokens)


def encode_decode_text(text):
  clean_text = re.sub(r'[^\x00-\x7F]+', '', text).strip()
  if clean_text:
    audio_signal = encode_phrase(clean_text)
    decoded_text = decode_phrase(audio_signal, 44100)
    return decoded_text
  else:
    return ''


if __name__ == '__main__':
  load_fingerprints()

  input_text = 'This is a sample text to encode and decode.'
  decoded_text = encode_decode_text(input_text)
  print('Input Text:', input_text)
  print('Decoded Text:', decoded_text)
