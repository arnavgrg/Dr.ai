import requests
import hmac
import base64
import json

API_ENDPOINT = 'https://healthservice.priaid.ch/'
AUTH_ENDPOINT = 'https://authservice.priaid.ch/login'
api_key = 'Xt43G_GMAIL_COM_AUT'
secret_key = 'Dy28NfYp4r6GPq53R'
hashed_credentials = hmac.new(secret_key.encode(),AUTH_ENDPOINT.encode())

def authorization():
    URL = AUTH_ENDPOINT
    headers = {
    'Authorization': "Bearer " + api_key + ":" + base64.b64encode(hashed_credentials.digest()).decode()
    }

    r = requests.post(url = URL, headers = headers)
    data = r.json()

    return data["Token"]

class Diagnosis:

    def __init__(self, gender, birth):
        self.gender = gender
        self.birth = birth
        self.token = authorization()

    def diagnosis(self, symptom_ids):
        PARAMS = {
        'symptoms': json.dumps(symptom_ids),
        'gender': self.gender,
        'year_of_birth': self.birth,
        "token": self.token,
        "language": 'en-gb'
        }
        URL = API_ENDPOINT + 'diagnosis'

        r = requests.get(url = URL, params = PARAMS)
        data = r.json()
        if len(data) > 0:
            result = {
                "ID": data[0]["Issue"]["ID"],
                "Name": data[0]["Issue"]["Name"],
                "ProfName": data[0]["Issue"]["ProfName"],
                "Accuracy": data[0]["Issue"]["Accuracy"],
                "Specialisation": [spec["Name"] for spec in data[0]["Specialisation"] if spec["ID"] != 15],
                "Info": self.issue_info(data[0]["Issue"]["ID"])
            }
        else:
            result = None
        return result

    def proposed_symptoms(self, symptom_ids):
        PARAMS = {
        'symptoms': json.dumps(symptom_ids),
        'gender': self.gender,
        'year_of_birth': self.birth,
        "token": self.token,
        "language": 'en-gb'
        }

        URL = API_ENDPOINT + 'symptoms/proposed'

        r = requests.get(url = URL, params = PARAMS)
        data = r.json()
        return data[:2] if len(data) >= 2 else data

    def issue_info(self, issue_id):
        PARAMS = {
        'token': self.token,
        'language': 'en-gb'
        }

        URL = API_ENDPOINT + 'issues/' + str(issue_id) + "/info"

        r = requests.get(url = URL, params = PARAMS)
        data = r.json()

        return data

    def red_flag(self, symptom_id):
        PARAMS = {
        'symptomId': symptom_id,
        'token': self.token,
        'language': 'en-gb'
        }

        URL = API_ENDPOINT + "redflag"

        r = requests.get(url = URL, params = PARAMS)
        data = r.json()

        return True if len(data) > 0 else False
