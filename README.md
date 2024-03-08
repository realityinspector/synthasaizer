# synthasaizer

## scrapbook code 

We are going to find that mapping markov-like progression of tokens in networks will lead us to using fourier-like unpacking of "harmonics" of tokens to compress large-scale real-time streams of LLM-like AIs?

these don't work. 


# claude description of code: 

"Audio-based Text Encoding and Decoding

This project demonstrates a method for encoding text into audio signals and decoding the audio signals back into text. The encoding process assigns unique audio fingerprints to each token (word) in the input text, and the decoding process identifies the closest matching token based on the audio features extracted from the encoded audio signal.
Files

### token2tone.py: 
This script generates unique audio fingerprints for each token. It assigns a unique frequency, amplitude, duration, and wave type to each token based on its index in the token list.
    
### corrected_token2tone.py: 
This script is an updated version of token2tone.py with some corrections and improvements.
    
### encoder.py: 
This script takes a phrase as input, splits it into tokens, and generates an audio signal by concatenating the audio fingerprints of each token. It also adds click tracks between the tokens for separation. The resulting audio signal is saved as a WAV file.
    
### decoder.py: 
This script loads the encoded audio file and the audio fingerprints JSON file. It identifies the click tracks in the audio signal to separate the tokens. For each token segment, it extracts audio features (dominant frequency, amplitude, duration, and wave type) and finds the closest matching token from the fingerprints based on these features. Finally, it reconstructs the original phrase by joining the decoded tokens.
    
### modified_decoder.py: 
This script is a modified version of decoder.py with some additional comments and explanations.

## Usage

Generate audio fingerprints for your desired set of tokens using token2tone.py or corrected_token2tone.py. The generated fingerprints will be stored in a JSON file.
    
Use encoder.py to encode a text phrase into an audio signal. Provide the phrase and the audio fingerprints JSON file as input. The encoded audio will be saved as a WAV file.
    
Use decoder.py or modified_decoder.py to decode the encoded audio signal back into text. Provide the encoded audio WAV file and the audio fingerprints JSON file as input. The script will output the decoded phrase.

Note: Make sure to have the required dependencies installed (numpy, soundfile, scipy) before running the scripts.
Future Improvements

Enhance the wave type identification method in the decoder to accurately distinguish between different wave types.
    
Explore more advanced audio feature extraction techniques to improve the robustness of the encoding and decoding process.
    
Optimize the audio fingerprint generation process to handle a larger vocabulary and reduce potential collisions between similar-sounding tokens.
    
Investigate the use of error correction techniques to handle potential errors in the decoding process.
" 


Everything has some consciousness, and we tap into that. It is about energy at its most basic level.

Robert Moog
