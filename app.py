from flask import render_template, request
from flask import Flask
from flask import jsonify
from conversation_flow import flow
import read_audio
import os

app = Flask(__name__)
conversation = flow.Conversation()

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
def process_response():
    request.get_data()
    data = request.data.decode('utf-8')
    print(data)
    response = conversation.conversation(4, data)
    print(response)
    res = read_audio.text_to_speech(response['next_text'])
    print(res)
    return jsonify({"data": res})

@app.route('/conversation', methods=['POST'])
def talk():
    request.get_data()
    data = request.data
    res = conversation.conversation(data["step"],["text"])
    return jsonify(res)


if __name__ == "__main__":
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = "1"
    app.run(debug=True)
