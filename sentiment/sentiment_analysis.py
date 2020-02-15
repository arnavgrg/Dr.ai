from google.cloud import language_v1
from google.cloud.language_v1 import enums
import requests
import json

API_KEY = 'AIzaSyAM8K8pbreod8u0NuIgYxtgAwlYI9NDFbM'
API_ENDPOINT = 'https://language.googleapis.com/v1/documents:analyzeSentiment'

def sample_analyze_sentiment(text_content):

    URL = API_ENDPOINT

    type_ = enums.Document.Type.PLAIN_TEXT
    language = "en"

    document = {"content": text_content, "type": type_, "language": language}
    encoding_type = enums.EncodingType.UTF8

    data = {
    'document': document,
    'encodingType': encoding_type
    }

    r = requests.post(url = URL, data = json.dumps(data), params = {'key': API_KEY})

    response = r.json()
    score = response["documentSentiment"]["score"]

    if score > 0.25:
        return 1
    if score < -0.25:
        return -1
    return 0
