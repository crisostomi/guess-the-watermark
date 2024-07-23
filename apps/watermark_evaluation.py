import streamlit as st
import os
import random
from collections import defaultdict
import soundfile as sf
import streamlit as st
from pathlib import Path
from pydub import AudioSegment
import random
import os
from io import BytesIO

FOLDER_PATH = Path("data/examples")


# Helper function to load and play audio files
def load_audio(file_path):
    audio = AudioSegment.from_wav(file_path)
    buffer = BytesIO()
    audio.export(buffer, format="wav")
    buffer.seek(0)
    return buffer


# Helper function to get the list of audio pairs
def get_audio_pairs(folder_path):
    audio_files = os.listdir(folder_path)
    pairs = {}
    for file in audio_files:
        parts = file.split("_")
        some_id = parts[0]
        i = parts[1]
        key = f"{some_id}_{i}"
        if key not in pairs:
            pairs[key] = {}
        if "original" in file:
            pairs[key]["original"] = file
        elif "watermarked" in file:
            pairs[key]["watermarked"] = file
    return pairs


# Initialize session state
if "predictions" not in st.session_state:
    st.session_state.predictions = []

# Main app
st.title("Audio Watermark Detection")

# Load audio pairs
audio_pairs = get_audio_pairs(FOLDER_PATH)

# Select a random audio pair
key = random.choice(list(audio_pairs.keys()))
original_file = FOLDER_PATH / audio_pairs[key]["original"]
watermarked_file = FOLDER_PATH / audio_pairs[key]["watermarked"]

# Randomly decide which one to present first
if random.random() < 0.5:
    first_audio, second_audio = original_file, watermarked_file
    first_label, second_label = "original", "watermarked"
else:
    first_audio, second_audio = watermarked_file, original_file
    first_label, second_label = "watermarked", "original"

# Play the audio files
st.audio(load_audio(first_audio), format="audio/wav")
st.audio(load_audio(second_audio), format="audio/wav")

# User input
user_choice = st.radio("Which one is watermarked?", ("First", "Second"))

# Process the prediction
if st.button("Submit"):
    prediction = {
        "key": key,
        "first_label": first_label,
        "second_label": second_label,
        "user_choice": user_choice,
    }
    st.session_state.predictions.append(prediction)

# Compute metrics
if st.session_state.predictions:
    total = len(st.session_state.predictions)
    correct = 0
    false_positive = 0
    false_negative = 0

    for prediction in st.session_state.predictions:
        if (
            prediction["user_choice"] == "First"
            and prediction["first_label"] == "watermarked"
        ):
            correct += 1
        elif (
            prediction["user_choice"] == "Second"
            and prediction["second_label"] == "watermarked"
        ):
            correct += 1
        elif (
            prediction["user_choice"] == "First"
            and prediction["first_label"] == "original"
        ):
            false_positive += 1
        elif (
            prediction["user_choice"] == "Second"
            and prediction["second_label"] == "original"
        ):
            false_positive += 1
        elif (
            prediction["user_choice"] == "First"
            and prediction["first_label"] == "watermarked"
        ):
            false_negative += 1
        elif (
            prediction["user_choice"] == "Second"
            and prediction["second_label"] == "watermarked"
        ):
            false_negative += 1

    accuracy = correct / total
    st.write(f"Total: {total}")
    st.write(f"Correct: {correct}")
    st.write(f"Accuracy: {accuracy:.2f}")
