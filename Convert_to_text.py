import time

######
import speech_recognition as sr
import ffmpeg
from pydub import AudioSegment
import pydub 
import requests
import urllib
import os
######

def solve_captcha(SRC):
    src = SRC
    path_to_mp3 = os.path.normpath(os.path.join(os.getcwd(), "sample.mp3"))
    path_to_wav = os.path.normpath(os.path.join(os.getcwd(), "sample.wav"))

    urllib.request.urlretrieve(src, path_to_mp3)
    AudioSegment.converter = r"C:\PATH_Programs\ffmpeg.exe"
    AudioSegment.ffmpeg = r"C:\PATH_Programs\ffmpeg.exe"
    AudioSegment.ffprobe =r"C:\PATH_Programs\ffprobe.exe"


    sound = pydub.AudioSegment.from_mp3(path_to_mp3)
    sound.export(path_to_wav, format="wav")
    sample_audio = sr.AudioFile(path_to_wav)

    r = sr.Recognizer()
    with sample_audio as source:
        audio = r.record(source)
    try:
        key = r.recognize_google(audio,language = 'en-US')
        print("Generated text successfully")
    except sr.UnknownValueError:
        try:
            print("Google failed to generate text\ntrying with Bing...")
            key = r.recognize_bing(audio)
            print("text generated successfully with bing...")
        except TypeError:
            print("Audio recording inaudible :( \nReloading page...")
            key = None

    return key

