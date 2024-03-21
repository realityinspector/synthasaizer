import json
import numpy as np
import multiprocessing as mp

def generate_audio_fingerprint(index_token_tuple, total_tokens, config):
    index, token = index_token_tuple
    base_frequency = 300
    max_frequency = 3000
    frequency_step = (max_frequency - base_frequency) / total_tokens

    frequency = base_frequency + frequency_step * index
    amplitude = config['volumes'][index % len(config['volumes'])]
    duration = 0.1
    wave_type = config['wave_types'][index % len(config['wave_types'])]
    harmonics = config['harmonics'][index % len(config['harmonics'])]

    return {
        'token': token,
        'frequency': float(frequency),
        'amplitude': float(amplitude),
        'duration': float(duration),
        'wave_type': wave_type,
        'harmonics': int(harmonics)
    }

def generate_fingerprints(model, config):
    word_count = model['word_count']
    tokens = ['word' + str(i) for i in range(word_count)]

    with mp.Pool() as pool:
        fingerprints = pool.starmap(generate_audio_fingerprint,
                                    [(index_token, word_count, config) for index_token in enumerate(tokens)])

    output_file = f"{config['output_dir']}/audio_fingerprints_{model['name']}.json"
    with open(output_file, 'w') as file:
        json.dump(fingerprints, file, indent=2)

    print(f"Generated audio fingerprints for model: {model['name']}")

def main():
    with open('config.json', 'r') as file:
        config = json.load(file)

    for model in config['models']:
        generate_fingerprints(model, config)

if __name__ == '__main__':
    main()