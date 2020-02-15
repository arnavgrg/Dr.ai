from flask import render_template
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Flask app is working"


@app.route('/query')
def get():
    return render_template('base.html')
