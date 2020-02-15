''' Functions for symptom matching between user and database '''
import json
from bert_serving.client import BertClient
import pickle

SYMPTOMS_FILE = "../symptoms.json"


def parse_symptoms():
    ''' Parse symptoms and run it through bert '''
    bc = BertClient(check_length=False)

    with open(SYMPTOMS_FILE) as f:
        symptoms = json.load(f)

    symptoms = symptoms.keys()
    encodings = bc.encode(symptoms)

    print(encodings[0])
    print(len(encodings))

def matched_symptoms(user_text):
    known_symptoms = load_symptoms()
    query_words = set(user_text.lower().split())
    return query_words.intersection(known_symptoms)


#print(matched_symptoms('I might be catching the flu'))
if __name__ == "__main__":
    parse_symptoms()
