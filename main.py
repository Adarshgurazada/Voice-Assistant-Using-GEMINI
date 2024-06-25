import pyaudio
import struct

import pvporcupine as pv
import azure.cognitiveservices.speech as speechsdk
import google.generativeai as genai

from os import getenv
from dotenv import load_dotenv

load_dotenv()

PORCUPINE = getenv("PORCUPINE")
porcupine = pv.create(access_key=PORCUPINE, keywords=["jarvis"])

AZURE = getenv("AZURE")
speech_config = speechsdk.SpeechConfig(subscription=AZURE, region="centralindia")
speech_config.speech_synthesis_voice_name = "en-US-BrianMultilingualNeural"
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)


generation_config = {
  "temperature": 0.7,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 1024, 
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  },
]

GEMINI = getenv("GOOGLE_API")
genai.configure(api_key=GEMINI)
model = genai.GenerativeModel('gemini-1.5-flash-latest',generation_config=generation_config, safety_settings=safety_settings)

# Initialize chat with an empty history
chat = model.start_chat(history=[])

# Hardcoded context
context = "You are an Obidient Chat Assistant. You are a used to power a rover bot which can scout around an industrial area and pick things up. You should answer with great accuracy and utmost precision. You have to answer short and to the point with a little bit of pinache. You should always refer to me as BOSS"
chat.send_message(context)

def speech_to_text() -> str | None:
    result = speech_recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return 
    elif result.reason == speechsdk.ResultReason.Canceled:
        return
    

def text_to_speech(text:str) -> None:
    result = speech_synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error Details: {}".format(cancellation_details.error_details))


p = pyaudio.PyAudio()
stream = p.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length,
)

first_wake_word = True

while True:
    pcm = stream.read(porcupine.frame_length)
    pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

    wake_word_heard = porcupine.process(pcm) >= 0

    if not wake_word_heard:
        continue
    
    print("Jarvis Activated")

    if first_wake_word:
        text_to_speech("Activated. Ask me anything.")
        first_wake_word = False # Set to False after first wake word
    else:
        print("Listening for speech")
        text = speech_to_text()

        if text is None:
            print("No speech detected.")
            continue

        print("Transcription: " + text)

        # Get token count for the prompt
        prompt_tokens = model.count_tokens(text)
        print(f"Prompt tokens: {prompt_tokens}")

        # Send the user prompt
        response = chat.send_message(text)

        # Remove asterisks from the response
        cleaned_response = response.text.replace("*", "") 

        # Get token count for the response
        response_tokens = model.count_tokens(cleaned_response)
        print(f"Response tokens: {response_tokens}")

        print(cleaned_response)
        print()

        text_to_speech(cleaned_response)