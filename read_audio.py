import speech_recognition as sr
from gtts import gTTS
import os
import pygame
import houndify

# use the audio file as the audio source
r = sr.Recognizer()

HOUNDIFY_CLIENT_ID = "94iXzZrdKCISkoWU-y1teQ=="  # Houndify client IDs are Base64-encoded strings
HOUNDIFY_CLIENT_KEY = "_7OwfiGjU6q8ppWY5NuP7AikDNt9JQo02ke3nNv39leZNz8DPwxZyOOO9Oh6ErMrvRKv8NFk_aOPiUhfQ4kxIA=="
client = houndify.TextHoundClient(HOUNDIFY_CLIENT_ID, HOUNDIFY_CLIENT_KEY, "test")
# Houndify client keys are Base64-encoded strings


# use Microphone to record live Speech
def record_query():
    with sr.Microphone() as source:
        print('Say Something!')
        audio = r.listen(source)
        print('Done!')

# Read entire recorded audio source and send it through Google api
    text = r.recognize_houndify(audio)
# Print the Translated text
    print(text)

def text_to_speech(text, language='en'):

    # Passing the text and language to the engine,
    # here we have marked slow=False. Which tells
    # the module that the converted audio should
    # have a high speed
    myobj = gTTS(text=text, lang=language, slow=False)

    # Saving the converted audio in a mp3 file named
    # welcome
    try:
        myobj.save("")
    except:
        print("Error writing string to mp3")

    # Playing the converted file
    pygame.mixer.init()
    os.system("mpg321 welcome.mp3")

