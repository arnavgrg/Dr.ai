import numpy as np

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

def __init__():
    self.user_info = {
        "name": None,
        "age": None,
        "gender": None,
        "symptoms": None,
        "issue": None,
        "specialist": None
    }
    self.proposed_symptom = [None, None]
    self.severity = None
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
        "You should visit a " + self.user_info["specialist"] + ". Do you want us to connect you to an available " + self.user_info["specialist"] + " for a video call ?"
    }

def conversation(self, step, text):
    next_step = step + 1
    if step > 0:
        extractor = step_fun[step]
        var = extractor(text)
        if var != None:
            if step == 1:
                self.user_info["name"] = var
            elif step == 2:
                self.user_info["age"] = var
            elif step == 3:
                self.user_info["gender"] = var
            elif step == 5:
                self.user_info["symptoms"] = var
                self.proposed_symptom = proposed_symptoms(var.keys())
            elif step == 6:
                if var == True:
                    self.user_info["symptoms"][self.proposed_symptom[0]["ID"]] = {"Name": self.proposed_symptom[0]["Name"], "red_flag": None}
            elif step == 7:
                if var == True:
                    self.user_info["symptoms"][self.proposed_symptom[1]["ID"]] = {"Name": self.proposed_symptom[1]["Name"], "red_flag": None}
                diagnostic = diagnosis(self.user_info["symptoms"].keys())
                self.user_info["issue"] = {"Name": diagnostic["Name"], "Description": None}
                self.specialist = diagnostic["Specialisation"]
                for symptom_id in self.user_info["symptoms"].keys():
                    self.user_info["symptoms"][symptom_id]["red_flag"] = red_flag(symptom_id)
                red_flag = [self.user_info["symptoms"][s]["red_flag"] for s in self.user_info["symptoms"].keys()]
                self.severity = any(red_flag)
                self.user_info["issue"]["Description"] = issue_info(diagnostic["ID"])["Description"]
            else:
                return {"video_call": var}
            if step < 4:
                next_text = np.random.choice(self.sentence_flow[step+1])
            elif step == 4:
                next_text = self.sentence_flow[step+1][var]
            else:
                next_text = self.sentence_flow[step+1]
        else:
            next_text = self.sentence_flow[0]
            next_step = step
    else:
        next_text = np.random.choice(self.sentence_flow[step+1])
    return {"user_info": self.user_info, "next_text": next_text, "next_step": next_step}
