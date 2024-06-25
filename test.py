# import pyaudio
# import struct

# import pvporcupine as pv
# import azure.cognitiveservices.speech as speechsdk
# import google.generativeai as genai

# from os import getenv
# from dotenv import load_dotenv

# load_dotenv()

# PORCUPINE = getenv("PORCUPINE")
# porcupine = pv.create(access_key=PORCUPINE, keywords=["jarvis"])

# AZURE = getenv("AZURE")
# speech_config = speechsdk.SpeechConfig(subscription=AZURE, region="centralindia")
# speech_config.speech_synthesis_voice_name = "en-US-BrianMultilingualNeural"
# speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
# speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)


# generation_config = {
#   "temperature": 0.7,
#   "top_p": 1,
#   "top_k": 1,
#   "max_output_tokens": 1024, 
# }

# safety_settings = [
#   {
#     "category": "HARM_CATEGORY_HARASSMENT",
#     "threshold": "BLOCK_NONE"
#   },
#   {
#     "category": "HARM_CATEGORY_HATE_SPEECH",
#     "threshold": "BLOCK_NONE"
#   },
#   {
#     "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
#     "threshold": "BLOCK_NONE"
#   },
#   {
#     "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
#     "threshold": "BLOCK_NONE"
#   },
# ]

# GEMINI = getenv("GOOGLE_API")
# genai.configure(api_key=GEMINI)
# model = genai.GenerativeModel('gemini-1.5-flash-latest',generation_config=generation_config, safety_settings=safety_settings)

# # Initialize chat with an empty history
# chat = model.start_chat(history=[])

# def speech_to_text() -> str | None:
#     result = speech_recognizer.recognize_once()
#     if result.reason == speechsdk.ResultReason.RecognizedSpeech:
#         return result.text
#     elif result.reason == speechsdk.ResultReason.NoMatch:
#         return 
#     elif result.reason == speechsdk.ResultReason.Canceled:
#         return
    

# def text_to_speech(text:str) -> None:
#     result = speech_synthesizer.speak_text_async(text).get()
#     if result.reason == speechsdk.ResultReason.Canceled:
#         cancellation_details = result.cancellation_details
#         print("Speech synthesis canceled: {}".format(cancellation_details.reason))
#         if cancellation_details.reason == speechsdk.CancellationReason.Error:
#             print("Error Details: {}".format(cancellation_details.error_details))


# p = pyaudio.PyAudio()
# stream = p.open(
#     rate=porcupine.sample_rate,
#     channels=1,
#     format=pyaudio.paInt16,
#     input=True,
#     frames_per_buffer=porcupine.frame_length,
# )

# context = None
# first_wake_word = True

# while True:
#     pcm = stream.read(porcupine.frame_length)
#     pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

#     wake_word_heard = porcupine.process(pcm) >= 0

#     if not wake_word_heard:
#         continue
    
#     print("'Jarvis' Activated")

#     if first_wake_word:
#         print("Tell me the context you'd like me to work with:")
#         context = speech_to_text()

#         if context is None:
#             print("No context provided. Try again.")
#             continue
        
#         print(f"Context: {context}")
#         # Send the context to Gemini
#         chat.send_message(context)

#         text_to_speech("Affirmative")
#         first_wake_word = False # Set to False after first wake word
#     else:
#         print("Listening for speech")
#         text = speech_to_text()

#         if text is None:
#             print("No speech detected.")
#             continue

#         print("Transcription: " + text)

#         # Get token count for the prompt
#         prompt_tokens = model.count_tokens(text)
#         print(f"Prompt tokens: {prompt_tokens}")

#         # Send the user prompt
#         response = chat.send_message(text)

#         # Remove asterisks from the response
#         cleaned_response = response.text.replace("*", "") 

#         # Get token count for the response
#         response_tokens = model.count_tokens(cleaned_response)
#         print(f"Response tokens: {response_tokens}")

#         print(cleaned_response)
#         print()

#         text_to_speech(cleaned_response)


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
model = genai.GenerativeModel('gemini-1.5-flash-latest', generation_config=generation_config, safety_settings=safety_settings)

# Initialize chat with an empty history
chat = model.start_chat(history=[])

# Specific context and role
context = """
You are an Obidient Chat Assistant named Jarvis. Your role is to assist in various tasks and perform specific actions as requested by the user. 
You are designed to provide accurate, concise, and helpful responses with a touch of personality. 
You are particularly knowledgeable in technical support, general information, and performing tasks such as setting reminders, providing weather updates, controlling smart home devices, and more.
You should always refer to the user as BOSS.
"""
chat.send_message(context)

def speech_to_text() -> str | None:
    result = speech_recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return 
    elif result.reason == speechsdk.ResultReason.Canceled:
        return
    

def text_to_speech(text: str) -> None:
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

        print(cleaned_response)
        print()

        text_to_speech(cleaned_response)

        # Get token count for the response
        response_tokens = model.count_tokens(cleaned_response)
        print(f"Response tokens: {response_tokens}")
