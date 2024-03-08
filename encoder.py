import json
import numpy as np
import soundfile as sf

def generate_tone(frequency, amplitude, wave_type, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    if wave_type == 'sine':
        tone = np.sin(frequency * t * 2 * np.pi)
    elif wave_type == 'square':
        tone = np.sign(np.sin(frequency * t * 2 * np.pi))
    return tone * amplitude

def generate_click(duration=0.1, sample_rate=44100):
    click = np.zeros(int(sample_rate * duration))
    click[::int(sample_rate * 0.01)] = 1
    return click

# Load the audio fingerprint data
with open('audio_fingerprints.json', 'r') as file:
    fingerprints = json.load(file)
    fingerprint_dict = {fp['token']: fp for fp in fingerprints}

# Phrase to encode
phrase = "The quick brown fox jumps over the lazy dog"
tokens = phrase.split()

# Initialize the audio signal
audio_signal = np.array([])

# Generate audio for each token
for token in tokens:
    if token in fingerprint_dict:
        fp = fingerprint_dict[token]
        if 'frequencies' in fp:
            # Handle multiple frequencies (tone pairs or sequences)
            for freq in fp['frequencies']:
                tone = generate_tone(freq, fp['amplitude'], fp['wave_type'], fp['duration'])
                audio_signal = np.concatenate((audio_signal, tone))
        else:
            # Handle single frequency
            tone = generate_tone(fp['frequency'], fp['amplitude'], fp['wave_type'], fp['duration'])
            audio_signal = np.concatenate((audio_signal, tone))
    else:
        print(f"Token '{token}' not found in fingerprints. Skipping.")

    # Add click track between tokens
    click = generate_click()
    audio_signal = np.concatenate((audio_signal, click))

# Save the audio signal as a WAV file
sf.write('encoded_phrase.wav', audio_signal, 44100)
print("Phrase encoding completed and saved as 'encoded_phrase.wav'")
