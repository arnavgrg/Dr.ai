import numpy as np
import string 
import time
import json
import re

from bert_serving.client import BertClient
from sklearn.metrics.pairwise import cosine_similarity

import nltk
from nltk.tokenize import sent_tokenize

class TextSummarizer(object):
    def __init__(self, payload):
        self.payload = payload
        self.categories = ['i need a doctor', 'has the following symptoms', 'needs to show something']
        print("Attempting to connect to Bert instance.")
        self.bc = BertClient(check_length=False) #ip="52.249.61.86"
        print("Connected to Bert instance.")
        print("Server status:", self.bc.status)

    def get_paragraphs(self):
        text = self.payload #self.payload["data"]
        self.paragraphs = text.split("\n\n")
        self.sentences = []
        for paragraph in self.paragraphs:
            for sent in sent_tokenize(paragraph):
                self.sentences.append(sent)
        cleaned_sentences = []
        for sentence in self.sentences:
            if len(sentence.split()) > 2:
                cleaned_sentences.append(sentence)
        self.sentences = cleaned_sentences

    def lowercase_text(self):
        # lower case all words in sentences 
        for idx,sentence in enumerate(self.sentences):
            lower_cased_tokens = [word.lower() for word in sentence.split()]
            lower_cased_sentence = " ".join([word for word in lower_cased_tokens])
            if lower_cased_sentence:
                self.sentences[idx] = lower_cased_sentence.strip()
    
    def get_embeddings(self):
        self.question_embedding = self.bc.encode(self.sentences)
        self.category_embeddings = self.bc.encode(self.categories)
        self.length = len(self.categories)

    def build_similarity_matrix(self):
        self.similarity_matrix = np.zeros([self.length])
        for i in range(self.length):
            self.similarity_matrix[i] = cosine_similarity([self.question_embedding[0]], 
                                                                [self.category_embeddings[i]])

    def get_important_category(self):
        reversed_sorted = np.argsort(self.similarity_matrix)[::-1]
        top_similarity = reversed_sorted[0]
        return self.categories[top_similarity]

    def get_summary(self):
        ''' Returns a list of the most important sentences in the legal document. '''
        self.get_paragraphs()
        print("Cleaning text input")
        self.lowercase_text()
        print("Generating embeddings")
        self.get_embeddings()
        print("Building similarity matrix")
        self.build_similarity_matrix()
        print(self.similarity_matrix)
        summary = self.get_important_category()
        return summary

if __name__ == '__main__':
    data = "i feel naseous and have a headache and i've had a fever for the past few weeks and i am not sure what to do"
    a = TextSummarizer(data)
    print(a.get_summary())