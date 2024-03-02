from pydub import AudioSegment
import os
from google.cloud import speech
import io

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/LauB/Documents/Coding/visonary-scripts/cred/key.json"


def stereo_to_mono(audio_path):
    sound = AudioSegment.from_wav(audio_path)
    sound = sound.set_channels(1)  # Convert to mono
    sound.export(audio_path, format="wav")


def transcribe_file(speech_file, language="en-US"):
    # Convert stereo to mono
    stereo_to_mono(speech_file)

    # Instantiates a client
    client = speech.SpeechClient()

    # Loads the audio file into memory
    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio({
            "content": content
        })

    config = speech.RecognitionConfig({
        "encoding": speech.RecognitionConfig.AudioEncoding.LINEAR16,
        "sample_rate_hertz": 44100,
        "language_code": language,
    })

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))


# Example usage
transcribe_file("./data/harvard.wav")
