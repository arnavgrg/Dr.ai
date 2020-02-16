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

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/')
def index():
    step = 1
    return render_template('base.html')

@app.route('/query', methods=['POST', 'GET'])
def get():
    user_name = request.form.get('userName')
    return render_template('base.html', username=user_name)

@app.route('/response', methods=['POST'])
def talk():
    global step
    request.get_data()
    data = request.data
    res = conversation.conversation(step, data.decode('utf-8'))
    print(res)
    if step == 8:
        return render_template('details.html', user_info=res['user_info'])
    audio = read_audio.text_to_speech(res['next_text'])
    print(res['next_text'], res['next_step'])
    step = res['next_step']
    pprint.pprint(res)
    return jsonify({'data': audio})


if __name__ == "__main__":
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = "1"
    app.run(debug=True)
