from flask import render_template
from flask import Flask

app = Flask(__name__)
app.debug = True

@app.route('/') 
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST','GET'])
def get():
    return render_template('base.html')