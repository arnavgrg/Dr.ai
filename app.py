from flask import render_template, request
from flask import Flask
import os

app = Flask(__name__)

@app.route('/') 
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST','GET'])
def get():
    user_name = request.form.get('userName')
    return render_template('base.html', username=user_name)

if __name__ == "__main__":
    os.environ['FLASK_ENV']='development'
    os.environ['FLASK_DEBUG']="1"
    app.run(debug=True)