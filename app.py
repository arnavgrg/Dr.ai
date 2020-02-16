from flask import render_template, request
from flask import Flask
from flask import jsonify
from conversation_flow import flow
import read_audio
import os

app = Flask(__name__)
conversation = flow.Conversation()
step = 1

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/')
def index():
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
    audio = read_audio.text_to_speech(res['next_text'])
    print(res['next_text'], res['next_step'])
    step = res['next_step']
    return jsonify({'data': audio})


if __name__ == "__main__":
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = "1"
    app.run(debug=True)
