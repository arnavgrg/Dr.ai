
from flask import render_template, request
from flask import Flask
from read_audio import text_to_speech

app = Flask(__name__)

@app.route('/') 
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST','GET'])
def get():
    user_name = request.form.get('userName')
    return render_template('base.html', username=user_name)

@app.route('/response', methods=['POST'])
def process_response():
    data = request.get_json()
    text = data["text"]
    text_to_speech(text)

if __name__ == "__main__":
    app.run(debug=True)