import threading
import time
import numpy as np
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import tkinter as tk
import json
import os
import pandas as pd
import warnings
# Ignore the FutureWarning about the deprecation
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers")
# Ignore the model weight warning
warnings.filterwarnings("ignore", message="Some weights of Wav2Vec2ForCTC were not initialized", category=UserWarning)


# Define audio parameters
SAMPLE_RATE = 16000
CHANNELS = 1

# Load models
vosk_model = Model(r"D:\Documents0\Alexa Files\PythonProject\TessResearch\Program\Models\vosk-model-en-us-0.22")  # Replace with your Vosk model path
tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
wav2vec_model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

# Initialize variables
recording = False
audio_queue = []
words = [ "start", "stop", "skip",
        "see" , "look" , "mother" , "little" , "here" , "can" , "want" , "come" , "one" , "baby" , "three" , "run" , "jump" , "down" , "is" , "up" , "make" , "ball" , "help" , "play",
		"with" , "friends" , "came" , "horse" , "ride" , "under" , "was" , "what" , "bump" , "live" , "very" , "puppy" , "dark" , "first" , "wish" , "basket" , "food" , "road" , "hill" , "along",
		"game" , "hide" , "grass" , "across" , "around" , "breakfast" , "field" , "large" , "better" , "suddenly" , "happen" , "farmer" , "river" , "lunch" , "sheep" , "hope" , "forest" , "stars" , "heavy" , "station",
		"safe" , "against" , "smash" , "reward" , "evening" , "stream" , "empty" , "stone" , "grove" , "desire" , "ocean" , "bench" , "damp" , "timid" , "perform" , "destroy" , "delicious" , "hunger" , "excuse" , "understood",
		"harness" , "price" , "flakes" , "silence" , "develop" , "promptly" , "serious" , "courage" , "forehead" , "distant" , "anger" , "vacant" , "appearance" , "speechless" , "region" , "slumber" , "future" , "claimed" , "common" , "dainty",
		"cushion" , "generally" , "extended" , "custom" , "tailor" , "haze" , "gracious" , "dignity" , "terrace" , "applause" , "jungle" , "fragrant" , "interfere" , "marriage" , "profitable" , "define" , "obedient" , "ambition" , "presence" , "merchant",
		"installed" , "importance" , "medicine" , "rebellion" , "infected" , "responsible" , "liquid" , "tremendous" , "customary" , "malicious" , "spectacular" , "inventory" , "yearning" , "imaginary" , "consequently" , "excellence" , "dungeon" , "detained" , "abundant" , "compliments",
		"administer" , "tremor" , "environment" , "counterfeit" , "crisis" , "industrious" , "approximate" , "society" , "architecture" , "malignant" , "pensive" , "standardize" , "exhausted" , "reminiscence" , "intricate" , "contemporary" , "attentively" , "compassionate" , "complexion" , "continuously"]
results = []
current_word_index = 0  # Tracks the index of the current word in the array
display_count = 0  # Tracks the number of times the current word has been displayed

# Function to record audio continuously
def record_audio():
    global recording, audio_queue
    while recording:
        audio_chunk = sd.rec(int(SAMPLE_RATE * 2), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16')
        sd.wait()
        audio_queue.append(audio_chunk)

# Function for Vosk transcription
def transcribe_vosk():
    recognizer = KaldiRecognizer(vosk_model, SAMPLE_RATE)
    transcriptions = []
    for audio_data in audio_queue:
        recognizer.AcceptWaveform(audio_data.tobytes())
        result = json.loads(recognizer.Result()).get("text", "")
        transcriptions.append(result)
    return transcriptions

# Function for Wav2Vec transcription
def transcribe_wav2vec():
    transcriptions = []
    for audio_data in audio_queue:
        input_values = tokenizer(audio_data.flatten(), return_tensors="pt", padding="longest").input_values
        with torch.no_grad():
            logits = wav2vec_model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = tokenizer.batch_decode(predicted_ids)
        transcriptions.append(transcription[0])
    return transcriptions

def check_word(res, word):
    if word in res:
        return "X"
    else:
        return " "

# Function to save results in an Excel file
def save_results_to_excel():
    # Find the next available file name
    base_filename = "UITesting"
    file_number = 1
    while os.path.exists(f"{base_filename}{file_number}.xlsx"):
        file_number += 1
    filename = f"{base_filename}{file_number}.xlsx"

    # Convert results to DataFrame and save as Excel file
    data = []
    for result in results:
        data.append({
            "Word": result["word"],
            "Vosk Result": result["vosk_results"],
            "Vosk Check": check_word(result["vosk_results"], result["word"]),
            "Wav2Vec Result": result["wav2vec_results"],
            "Wav2Vec Check" : check_word(result["wav2vec_results"], result["word"].upper())
        })
    
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Results saved to {filename}")

# Function to toggle recording and show a new word
def toggle_recording():
    global recording, audio_queue, display_count, current_word_index, results

    if current_word_index >= len(words):
        # All words have been processed, save and stop
        save_results_to_excel()
        print("Results saved. All words have been processed.")
        record_button.config(state="disabled")
        return

    if recording:
        # Stop recording with a 1-second delay
        time.sleep(1)
        recording = False

        # Transcribe audio with Vosk and Wav2Vec
        vosk_results = transcribe_vosk()
        wav2vec_results = transcribe_wav2vec()

        # Append results for the current word
        results.append({
            "word": words[current_word_index],
            "vosk_results": vosk_results,
            "wav2vec_results": wav2vec_results
        })

        # Print individual transcription results for this cycle
        print(f"Word: {words[current_word_index]}, Display {display_count} of 3")
        print(f"Vosk Result: {vosk_results}")
        print(f"Wav2Vec Result: {wav2vec_results}")

        record_button.config(text="Start Recording")

        # Move to the next word if displayed three times
        if display_count == 3:
            display_count = 0
            current_word_index += 1

        # End condition after final word
        if current_word_index >= len(words):
            save_results_to_excel()  # Save all results when done
            word_label.config(text="")  # Clear word label
            count_label.config(text="")
            record_button.pack_forget()
            restart_button.pack(pady=10)
            exit_button.pack(pady=10)
        else:
            word_label.config(text="")

    else:
        # Start recording
        audio_queue = []  # Clear previous recordings
        recording = True
        record_thread = threading.Thread(target=record_audio)
        record_thread.start()
        record_button.config(text="Stop and Transcribe")

        # Show the current word in the separate window
        display_word_in_window(words[current_word_index])

# Function to display or update the word and count in the separate window
def display_word_in_window(word):
    global word_window, word_label, count_label, display_count

    # Update the word and increment the display count
    word_label.config(text=word)
    display_count += 1
    count_label.config(text=f"Tries: {display_count} of 3")

# Function to restart the sequence
def restart():
    global results, display_count, current_word_index
    results = []  # Reset all saved results
    display_count = 0
    current_word_index = 0
    record_button.pack(pady=20)
    restart_button.pack_forget()
    exit_button.pack_forget()
    word_label.config(text="")
    count_label.config(text="")

    # Reset the main window's record button
    record_button.config(text="Start Recording")

def stop():
    save_results_to_excel()
    restart()

# Set up tkinter UI
root = tk.Tk()
root.title("Audio Transcription with Flash Words")

# Create display elements
status_label = tk.Label(root, text="Press 'Start Recording' to see a word", font=("Helvetica", 24))
status_label.pack(expand=True)

record_button = tk.Button(root, text="Start Recording", command=toggle_recording)
stop_button = tk.Button(root, text="Stop", command=stop)
record_button.pack(pady=10)
stop_button.pack(pady=10)

restart_button = tk.Button(root, text="Restart", command=restart)
exit_button = tk.Button(root, text="Exit", command=root.quit)

# Create the word flash window immediately
word_window = tk.Toplevel(root)
word_window.title("Flash Word")
word_window.geometry("700x500")

# Create the labels for the word and the count
word_label = tk.Label(word_window, text="", font=("Helvetica", 150), fg="black")
word_label.pack(expand=True)

count_label = tk.Label(word_window, text="", font=("Helvetica", 16), fg="grey")
count_label.pack()

root.mainloop()
