from flask import render_template, request
from flask import Flask
from flask import jsonify
from flask import redirect, url_for
from conversation_flow import flow
import read_audio
import os
import pprint

app = Flask(__name__)
conversation = flow.Conversation()
step = 1
global_user_info = None

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/')
def index():
    # global global_user_info
    # global_user_info={'age': 20, 'gender': 'female', 'issue': {'Description': 'Vasculitis describes an inflammation ' 'of certain blood vessels, caused by ' 'the immune system. It can be ' 'accompanied by a number of conditions ' 'with different symptoms, depending on ' 'which organ or organ systems are ' 'affected. Either the arteries or the ' 'veins of any organ can be affected. ' 'It can be caused by a ' 'hypersensitivity reaction to certain ' 'medication or an immunological ' 'disease.', 'Name': 'Vascular inflammation', 'ProfName': 'Vasculitis', 'Specialists': ['Internal medicine', 'Rheumatology'], 'Treatment': 'Consequences and treatment depend on ' 'the type of vasculitis. Often, the ' 'initial treatment includes cortisone or ' 'another medication modulating the ' 'immune system, to reduce the ' 'inflammatory response. The respective ' 'treatments for specific conditions can ' 'be read in the medical article ' 'referring to that condition and it ' 'should be discussed with the treating ' 'doctor.'}, 'name': 'hey', 'symptoms': {14: {'Name': 'Runny nose', 'red_flag': False}, 16: {'Name': 'Tiredness', 'red_flag': False}, 978: {'Name': 'Cold hands', 'red_flag': False}}}
    # return redirect(url_for('metrics'))
    step = 1
    return render_template('base.html')

@app.route('/query', methods=['POST', 'GET'])
def get():
    user_name = request.form.get('userName')
    return render_template('base.html', username=user_name)


@app.route('/response', methods=['POST'])
def talk():
    global user_info
    global step
    request.get_data()
    data = request.data
    res = conversation.conversation(step, data.decode('utf-8'))
    print(res,step)
    if step == 8:
        #import ipdb; ipdb.set_trace()
        global_user_info = res['user_info']
        return redirect(url_for('metrics'))
        #return render_template('details.html', user_info=res['user_info'])
    audio = read_audio.text_to_speech(res['next_text'])
    print(res['next_text'], res['next_step'])
    step = res['next_step']
    pprint.pprint(res)
    return jsonify({'data': audio})

@app.route('/metrics', methods=['GET'])
def metrics():
    return render_template('details.html', user_info=global_user_info)

if __name__ == "__main__":
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = "1"
    app.run(debug=True)
