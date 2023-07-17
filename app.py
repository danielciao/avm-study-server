
import time

from flask import Flask
from modules.attribute_finder import LocationAttributeFinder

app = Flask(__name__)
finder = LocationAttributeFinder()


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/ping')
def get_current_time():
    return {'pong': time.time()}


@app.route('/status')
def get_load_status():
    return finder.get_load_status()
