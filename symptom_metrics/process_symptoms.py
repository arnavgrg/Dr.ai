''' Functions for symptom matching between user and database '''
import json
from bert_serving.client import BertClient
import pickle
import numpy as np
import spacy
import string

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

nltk.download('stopwords')
stop_words = set(stopwords.words('english')) - {"up"}

SYMPTOMS_FILE = "symptoms.json"
symptoms = None

nlp = spacy.load('en', disable=['parser', 'ner'])

def parse_symptoms(user_text):
    ''' Parse symptoms and run it through bert '''
    bc = BertClient(check_length=False)

    with open(SYMPTOMS_FILE) as f:
        symptoms = json.load(f)

    user_text = user_text.translate(str.maketrans('', '', string.punctuation))
    new_user_text = ""
    for token in nlp(user_text):
        if token.lemma_ != '-PRON-':
            new_user_text += token.lemma_ + " "
    word_tokens = word_tokenize(new_user_text.strip()) 
    filtered_sentence = " ".join([w for w in word_tokens if not w in stop_words])

    symptoms = list(symptoms.keys())
    symptom_sentences = list()
    for symptom in symptoms:
        word_tokens = word_tokenize(symptom.strip())
        sentence = " ".join([w for w in word_tokens if not w in stop_words])
        symptom_sentences.append(sentence)

    encodings = bc.encode(symptoms)
    user_text_new = bc.encode([filtered_sentence.strip()])
    length = len(encodings)
    
    return symptoms, user_text_new, encodings, length

def build_similarity_matrix(user_text, known_symptoms, length):
    similarity_matrix = cosine_similarity(user_text, known_symptoms)
    return similarity_matrix[0]

def get_top_k_indexes(similarity_matrix, k):
    sorted_ = sorted(similarity_matrix)[::-1]
    print(sorted_[:k])
    reversed_sorted = np.argsort(similarity_matrix)[::-1]
    top_similarity = reversed_sorted[:k]
    return top_similarity

def matched_symptoms(user_text):
    symptoms, user_text_new, known_symptoms, length = parse_symptoms(user_text)
    similarity_matrix = build_similarity_matrix(user_text_new, known_symptoms, length)
    indexes = get_top_k_indexes(similarity_matrix, 5)
    for index in indexes:
        print(symptoms[index])

if __name__ == "__main__":
    matched_symptoms("I got high fever last week and have been in bed ever since.")

#"I got high fever last week and have been in bed ever since."
#"I have a had a bad cold for a week and think I am developing a fever"
#"I have a bad headache today."
#"I've had runny stools and stomach pain."
#"I am not feeling well. I have a stomach ache and a little bit of fever."
#"I woke up this morning thinking I would faint and then ended up throwing up."