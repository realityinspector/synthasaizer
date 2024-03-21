
import json
import os
from modified_token2tone import generate_audio_fingerprint
from encoder import encode_phrase
from modified_decoder import decode_phrase

def generate_test_tokens(number_of_tokens):
    return [{'string': f'token{i}', 'id': i} for i in range(number_of_tokens)]

def save_fingerprints(fingerprints, filename):
    with open(filename, 'w') as file:
        json.dump(fingerprints, file)

def run_tests(test_phrases, fingerprints_file, encoded_file):
    log_entries = []

    for phrase in test_phrases:
        # Encoding
        encode_phrase(phrase, fingerprints_file, encoded_file)

        # Decoding
        decoded_phrase = decode_phrase(encoded_file, fingerprints_file)

        # Logging the result
        success = phrase == decoded_phrase
        log_entries.append(f'Phrase: {phrase}, Decoded: {decoded_phrase}, Success: {success}')

    return log_entries

def write_log(log_entries, log_file):
    with open(log_file, 'w') as file:
        for entry in log_entries:
            file.write(f'{entry}\n')

# Example usage
if __name__ == "__main__":
    # Generate and save fingerprints
    test_tokens = generate_test_tokens(100)
    fingerprints = [generate_audio_fingerprint(token, i, len(test_tokens)) for i, token in enumerate(test_tokens)]
    save_fingerprints(fingerprints, 'audio_fingerprints.json')

    # Define test phrases
    test_phrases = ['token1 token2', 'token3 token4', 'token5 token6']

    # Run tests
    log_entries = run_tests(test_phrases, 'audio_fingerprints.json', 'encoded_phrase.wav')

    # Write log file
    write_log(log_entries, 'test_log.txt')
