import speech_recognition as sr
import os
import base64
import json
from google.cloud import texttospeech
import requests

# HOUNDIFY
# HOUNDIFY_CLIENT_ID = "94iXzZrdKCISkoWU-y1teQ=="  # Houndify client IDs are Base64-encoded strings
# HOUNDIFY_CLIENT_KEY = "_7OwfiGjU6q8ppWY5NuP7AikDNt9JQo02ke3nNv39leZNz8DPwxZyOOO9Oh6ErMrvRKv8NFk_aOPiUhfQ4kxIA=="
# userId = "test_user"
# requestInfo = {
#   "Latitude": 37.388309,
#   "Longitude": -121.973968,
#   "ResponseAudioVoice": "Judy",
#   "ResponseAudioShortOrLong": "Short"
# }
# 
# client = houndify.TextHoundClient(HOUNDIFY_CLIENT_ID, HOUNDIFY_CLIENT_KEY, userId, requestInfo)
# Houndify client keys are Base64-encoded strings

# google gTTS


def text_to_speech(text):
    input = {"text": text}
    voice = {"languageCode": "en-US", "ssmlGender": "FEMALE"}
    config = {"audioEncoding": "MP3"}
    data = {'input':input, 'voice':voice, 'audioConfig':config}
    response = requests.post('https://texttospeech.googleapis.com/v1/text:synthesize', data=json.dumps(data), params={'key': "AIzaSyDD1PgNuUQGbCanfVPYT0K2re94Dxv8kYU"})
    return json.loads(response.text)['audioContent']


