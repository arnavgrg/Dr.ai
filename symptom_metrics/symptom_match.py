''' Functions for symptom matching between user and database '''

def parse_symptoms_file(symptom_file):
    ''' Parse symptoms from symptoms.json and return it '''
    ##TODO
    return {}

def matched_symptoms(user_text):
    known_symptoms = parse_symptoms_file('./symptoms.json')
    query_words = set(user_text.lower().split())
    return query_words.intersection(known_symptoms)

print(matched_symptoms('I might be catching the flu'))
