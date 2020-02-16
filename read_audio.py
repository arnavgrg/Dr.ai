import speech_recognition as sr
import os
from gtts import gTTS
from houndify import houndify
import base64

# use the audio file as the audio source
r = sr.Recognizer()

HOUNDIFY_CLIENT_ID = "94iXzZrdKCISkoWU-y1teQ=="  # Houndify client IDs are Base64-encoded strings
HOUNDIFY_CLIENT_KEY = "_7OwfiGjU6q8ppWY5NuP7AikDNt9JQo02ke3nNv39leZNz8DPwxZyOOO9Oh6ErMrvRKv8NFk_aOPiUhfQ4kxIA=="
userId = "test_user"
requestInfo = {
  "Latitude": 37.388309,
  "Longitude": -121.973968,
  "ResponseAudioVoice": "Judy",
  "ResponseAudioShortOrLong": "Short"
}

client = houndify.TextHoundClient(HOUNDIFY_CLIENT_ID, HOUNDIFY_CLIENT_KEY, userId, requestInfo)
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

def text_to_speech(text):
    import ipdb; ipdb.set_trace()
    response = client.query(text)
    try:
        result = response["AllResults"][0]['ResponseAudioBytes']
    except:
        result = ''
    return result


