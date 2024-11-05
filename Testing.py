import threading
import time
import numpy as np
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

# Define audio parameters
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_DURATION = 2  # seconds

# Load models
vosk_model = Model(r"D:\Documents0\Alexa Files\PythonProject\TessResearch\Program\Models\vosk-model-en-us-0.22")  # Replace with your Vosk model path
tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
wav2vec_model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

# Function to record audio in chunks
def record_audio(queue):
    print("Recording audio...")
    for _ in range(int(5 / CHUNK_DURATION)):  # Record for 5 seconds
        audio_chunk = sd.rec(int(SAMPLE_RATE * CHUNK_DURATION), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16')
        sd.wait()  # Wait until the chunk is recorded
        queue.append(audio_chunk)
        time.sleep(CHUNK_DURATION)  # Sleep for the duration of the chunk

# Function for Vosk transcription
def transcribe_vosk(audio_queue):
    recognizer = KaldiRecognizer(vosk_model, SAMPLE_RATE)
    results = []
    for audio_data in audio_queue:
        recognizer.AcceptWaveform(audio_data.tobytes())
        result = recognizer.Result()
        results.append(result)
    return results

# Function for Wav2Vec transcription
def transcribe_wav2vec(audio_queue):
    results = []
    for audio_data in audio_queue:
        input_values = tokenizer(audio_data.flatten(), return_tensors="pt", padding="longest").input_values
        with torch.no_grad():
            logits = wav2vec_model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = tokenizer.batch_decode(predicted_ids)
        results.append(transcription[0])  # Return the first result
    return results

# Wrapper function to handle threading
def thread_function(queue, name):
    time.sleep(1)  # Ensure recording is ready
    if name == "Vosk":
        result = transcribe_vosk(queue)
    elif name == "Wav2Vec":
        result = transcribe_wav2vec(queue)
    print(f"{name} Result: {result}")

# Main function to start the comparison
def main():
    audio_queue = []
    
    # Start audio recording thread
    record_thread = threading.Thread(target=record_audio, args=(audio_queue,))
    record_thread.start()
    
    # Wait for recording to finish
    record_thread.join()

    # Start transcription threads
    threads = []
    for model_name in ["Vosk", "Wav2Vec"]:
        thread = threading.Thread(target=thread_function, args=(audio_queue, model_name))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
