''' Functions for symptom matching between user and database '''
import json
import bert

SYMPTOMS_FILE = "../symptoms.json"


def parse_symptoms():
    ''' Parse symptoms and run it through bert '''
    with open(SYMPTOMS_FILE) as f:
        symptoms = json.load(f)

    for symptom in symptoms.keys():
        bert


def matched_symptoms(user_text):
    known_symptoms = load_symptoms()
    query_words = set(user_text.lower().split())
    return query_words.intersection(known_symptoms)


print(matched_symptoms('I might be catching the flu'))
