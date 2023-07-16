
import time

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/ping')
def get_current_time():
    return {'pong': time.time()}
