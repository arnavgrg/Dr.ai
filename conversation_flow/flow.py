import numpy as np
import json
import sys
sys.path.append('../')
from symptom_metrics import diagnosis

def name_extractor(text):
    return np.random.choice([None, "John", "Peter", "Mike", "Tommy"])

def age_extractor(text):
    return np.random.choice([np.random.randint(1920, 2020), None])

def gender_extractor(text):
    return np.random.choice([None, "Male", "Female"])

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

def yes_no_extractor(text):
    return np.random.choice([None, True, False])

step_fun = {
    1: name_extractor,
    2: age_extractor,
    3: gender_extractor,
    4: analyze_sentiment,
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
                    self.diagnosis = diagnosis.Diagnosis(self.user_info["gender"], 2020-self.user_info["age"])
                elif step == 5:
                    self.user_info["symptoms"] = var
                    self.proposed_symptom = self.diagnosis.proposed_symptoms(list(var.keys()))
                    if len(self.proposed_symptom) == 0:
                        diagnostic = self.diagnosis.diagnosis(list(self.user_info["symptoms"].keys()))
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

text = None
step = 0
conversation = Conversation()
while step < 8:
    res = conversation.conversation(step,text)
    print(res["next_text"])
    step = res["next_step"]
    text = input()
res = conversation.conversation(step, text)
