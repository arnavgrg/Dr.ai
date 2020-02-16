import numpy as np
import json
import sys
import string
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
sys.path.append('../')
from symptom_metrics import diagnosis
from sentiment import sentiment_analysis as sa

def name_extractor(document):
    ''' Returns name, otherwise returns 1 if no name detected '''
    import ipdb; ipdb.set_trace()
    common_words = { 'hi','hello','my','name','is','good', 'morning',
                        'evening', 'afternoon', 'go', 'by'}
    document = " ".join([i for i in document.split() if i not in stop])
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    for item in sentences[0]:
        if item[1] == 'NNP' and item[0].lower() not in common_words:
            return item[0]
    return None

def age_extractor(document):
    ''' Returns age, otherwise returns 1 if no age keyword detected '''
    numbers = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20, 'twenty one': 21, 'twenty two': 22, 'twenty three': 23, 'twenty four': 24, 'twenty five': 25, 'twenty six': 26, 'twenty seven': 27, 'twenty eight': 28, 'twenty nine': 29, 'thirty': 30, 'thirty one': 31, 'thirty two': 32, 'thirty three': 33, 'thirty four': 34, 'thirty five': 35, 'thirty six': 36, 'thirty seven': 37, 'thirty eight': 38, 'thirty nine': 39, 'forty': 40, 'forty one': 41, 'forty two': 42, 'forty three': 43, 'forty four': 44, 'forty five': 45, 'forty six': 46, 'forty seven': 47, 'forty eight': 48, 'forty nine': 49, 'fifty': 50, 'fifty one': 51, 'fifty two': 52, 'fifty three': 53, 'fifty four': 54, 'fifty five': 55, 'fifty six': 56, 'fifty seven': 57, 'fifty eight': 58, 'fifty nine': 59, 'sixty': 60, 'sixty one': 61, 'sixty two': 62, 'sixty three': 63, 'sixty four': 64, 'sixty five': 65, 'sixty six': 66, 'sixty seven': 67, 'sixty eight': 68, 'sixty nine': 69, 'seventy': 70, 'seventy one': 71, 'seventy two': 72, 'seventy three': 73, 'seventy four': 74, 'seventy five': 75, 'seventy six': 76, 'seventy seven': 77, 'seventy eight': 78, 'seventy nine': 79, 'eighty': 80, 'eighty one': 81, 'eighty two': 82, 'eighty three': 83, 'eighty four': 84, 'eighty five': 85, 'eighty six': 86, 'eighty seven': 87, 'eighty eight': 88, 'eighty nine': 89, 'ninety': 90, 'ninety one': 91, 'ninety two': 92, 'ninety three': 93, 'ninety four': 94, 'ninety five': 95, 'ninety six': 96, 'ninety seven': 97, 'ninety eight': 98, 'ninety nine': 99, 'one hundred': 100}

    document = document.translate(str.maketrans('', '', string.punctuation)).lower()
    numbers_reverse = list(numbers.keys())
    numbers_reverse.reverse()
    for number in numbers_reverse:
        if number in document:
            return numbers[number]
    return None

def gender_extractor(document):
    ''' Returns detected gender, otherwise reutnrs 1 if no gender keyword was detected '''
    male = {'man','male','him','he','his','men'}
    female = {'female','woman','women','her','hers','she'}
    document = set(document.lower().split())
    if female.intersection(document):
        return "female"
    elif male.intersection(document):
        return "male"
    return "non-binary"

def analyze_sentiment(text):
    return np.random.choice([-1,0,1])

def symptoms_extractor(text):
    with open('../symptom_metrics/symptoms.json') as json_file:
        data = json.load(json_file)
    symptoms = list(data.keys())
    symptoms = np.random.choice(symptoms, np.random.randint(6))
    ans = {}
    for key in symptoms:
        ans[data[key]] = {"Name": key}

    return [None, ans][np.random.randint(2)]

def yes_no_extractor(document):
    ''' Returns yes/no from the document; In case of confusion, it returns no'''
    if 'yes' in document.lower() and 'no' not in document.lower():
        return True
    if 'no' in document.lower() and 'yes' not in document.lower():
        return False
    return None

step_fun = {
    1: name_extractor,
    2: age_extractor,
    3: gender_extractor,
    4: sa.analyze_sentiment,
    5: symptoms_extractor,
    6: yes_no_extractor,
    7: yes_no_extractor,
    8: yes_no_extractor
}

class Conversation:
    def __init__(self):
        self.user_info = {
            "name": "None",
            "age": 0,
            "gender": "None",
            "symptoms": "None",
            "issue": {"Name": "None", "Specialists": ["None"]}
        }
        self.proposed_symptom = [{"ID": None, "Name": "None"}, {"ID": None, "Name": "None"}]
        self.severity = 0
        self.diagnosis = None

    def update_sentence_flow(self):
        self.sentence_flow = {
        -1: "Based on your symptoms, I am not sure how to proceed. Do you want to connect to an available generalist for a video call ?",
        0: "Sorry, I'm in beta version and I didn't understand. Can you say it again ?",
        1: ["Hi, what is your name ?", "Hello, may I have your name ?", "Hi, could you tell me your name ?"],
        2: ["Nice to meet you, " + self.user_info["name"] + "! Can you tell me your age ?", "Glad to meet you, " + self.user_info["name"] + "! May I have your age, please ?",
        "Nice to meet you, " + self.user_info["name"] + "! How old are you ?"],
        3: ["Thank you, " + self.user_info["name"] + "! I need one more information from you. What is your gender ?",
        "Thanks, " + self.user_info["name"] + "! Last piece of information: Can I have your gender ?", "Perfect! Can you also tell me your gender ?"],
        4: ["Awesome! Now let's start. How has your day been ?", "Great! Now we can start. How was your day ?"],
        5: {1: "I'm glad to hear that your day has been good! How can I help you ? Do you have any symptoms you would like to share ?",
            0: "All right! How can I help you ? Do you have any symptoms you would like to share ?",
            -1: "I'm sorry to hear that. How can I help you ? Do you have any symptoms you would like to share ?"
              },
        6: "Do you also have " + self.proposed_symptom[0]["Name"] + "?",
        7: "And what about " + self.proposed_symptom[1]["Name"] + "?",
        8: "Based on what you said, you probably have " + self.user_info["issue"]["Name"] + "." + "This is a severe condition. You should go to the doctor immediately!" if self.severity == 1 else "This is not a severe condition, but I recommend you go to the doctor." +
            "You should visit a doctor in General Practice" + "".join([" or " + specialist for specialist in self.user_info["issue"]["Specialists"] if len(self.user_info["issue"]["Specialists"]) > 0]) + ". Do you want us to connect you to an available specialist for a video call ?"
        }

    def conversation(self, step, text):
        next_step = step + 1
        if step > 0:
            extractor = step_fun[step]
            var = extractor(text)
            boo = not type(var) == type(None)
            if boo:
                if step == 1:
                    self.user_info["name"] = var
                elif step == 2:
                    self.user_info["age"] = var
                elif step == 3:
                    self.user_info["gender"] = var
                    gender = self.user_info["gender"] if self.user_info["gender"] != "non-binary" else "female"
                    birth = 2020-self.user_info["age"]
                    self.diagnosis = diagnosis.Diagnosis(gender, birth)
                elif step == 5:
                    self.user_info["symptoms"] = var
                    self.proposed_symptom = self.diagnosis.proposed_symptoms(list(var.keys()))
                    if len(self.proposed_symptom) == 0:
                        diagnostic = self.diagnosis.diagnosis(list(self.user_info["symptoms"].keys()))
                        if type(diagnostic) == type(None):
                            return {"user_info": self.user_info, "next_text": self.sentence_flow[-1], "next_step": 8}
                        self.user_info["issue"] = {"Name": diagnostic["Name"], "ProfName": diagnostic["ProfName"], "Description": diagnostic["Info"]["DescriptionShort"], "Treatment": diagnostic["Info"]["TreatmentDescription"], "Specialists": diagnostic["Specialisation"]}
                        for symptom_id in self.user_info["symptoms"].keys():
                            self.user_info["symptoms"][symptom_id]["red_flag"] = self.diagnosis.red_flag(symptom_id)
                        red_flag = [self.user_info["symptoms"][s]["red_flag"] for s in self.user_info["symptoms"].keys()]
                        self.severity = any(red_flag)
                        self.update_sentence_flow()
                        return {"user_info": self.user_info, "next_text": self.sentence_flow[8], "next_step": 8}
                elif step == 6:
                    if var == True:
                        self.user_info["symptoms"][self.proposed_symptom[0]["ID"]] = {"Name": self.proposed_symptom[0]["Name"]}
                    if len(self.proposed_symptom) == 1:
                        diagnostic = self.diagnosis.diagnosis(list(self.user_info["symptoms"].keys()))
                        if type(diagnostic) == type(None):
                            return {"user_info": self.user_info, "next_text": self.sentence_flow[-1], "next_step": 8}
                        self.user_info["issue"] = {"Name": diagnostic["Name"], "ProfName": diagnostic["ProfName"], "Description": diagnostic["Info"]["DescriptionShort"], "Treatment": diagnostic["Info"]["TreatmentDescription"], "Specialists": diagnostic["Specialisation"]}
                        for symptom_id in self.user_info["symptoms"].keys():
                            self.user_info["symptoms"][symptom_id]["red_flag"] = self.diagnosis.red_flag(symptom_id)
                        red_flag = [self.user_info["symptoms"][s]["red_flag"] for s in self.user_info["symptoms"].keys()]
                        self.severity = any(red_flag)
                        self.update_sentence_flow()
                        return {"user_info": self.user_info, "next_text": self.sentence_flow[8], "next_step": 8}
                elif step == 7:
                    if var == True:
                        self.user_info["symptoms"][self.proposed_symptom[1]["ID"]] = {"Name": self.proposed_symptom[1]["Name"]}
                    diagnostic = self.diagnosis.diagnosis(list(self.user_info["symptoms"].keys()))
                    if type(diagnostic) == type(None):
                        return {"user_info": self.user_info, "next_text": self.sentence_flow[-1], "next_step": 8}
                    self.user_info["issue"] = {"Name": diagnostic["Name"], "ProfName": diagnostic["ProfName"], "Description": diagnostic["Info"]["DescriptionShort"], "Treatment": diagnostic["Info"]["TreatmentDescription"], "Specialists": diagnostic["Specialisation"]}
                    for symptom_id in self.user_info["symptoms"].keys():
                        self.user_info["symptoms"][symptom_id]["red_flag"] = self.diagnosis.red_flag(symptom_id)
                    red_flag = [self.user_info["symptoms"][s]["red_flag"] for s in self.user_info["symptoms"].keys()]
                    self.severity = any(red_flag)
                elif step == 8:
                    return {"video_call": var}
                if step < 4:
                    self.update_sentence_flow()
                    next_text = np.random.choice(self.sentence_flow[step+1])
                elif step == 4:
                    self.update_sentence_flow()
                    next_text = self.sentence_flow[step+1][var]
                else:
                    self.update_sentence_flow()
                    next_text = self.sentence_flow[step+1]
            else:
                self.update_sentence_flow()
                next_text = self.sentence_flow[0]
                next_step = step
        else:
            self.update_sentence_flow()
            next_text = np.random.choice(self.sentence_flow[step+1])

        return {"user_info": self.user_info, "next_text": next_text, "next_step": next_step}

if __name__ == "__main__":
    text = None
    step = 0
    conversation = Conversation()
    while step < 8:
        res = conversation.conversation(step,text)
        print(res["next_text"])
        step = res["next_step"]
        text = input()
    res = conversation.conversation(step, text)
    print(conversation.user_info)
