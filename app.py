from flask import render_template, request
from flask import Flask
from flask import jsonify
import read_audio
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/query', methods=['POST', 'GET'])
def get():
    user_name = request.form.get('userName')
    return render_template('base.html', username=user_name)


@app.route('/response', methods=['POST'])
def process_response():
    request.get_data()
    data = request.data
    print(data.decode('utf-8'))
    res = read_audio.text_to_speech(data.decode('utf-8'))
    return jsonify({"data": res})


if __name__ == "__main__":
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = "1"
    app.run(debug=True)
