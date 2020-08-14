import os
import time
import playsound
import pyaudio
import speech_recognition as sr
from gtts import gTTS

def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source=source,timeout=5,phrase_time_limit=5)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except LookupError:
            print("Could not understand")
     
    return said


text = get_audio()

if "hello" in text:
    speak("hello, how are you?")

if "what is your name" in text:
    speak("my name is Sofia")


