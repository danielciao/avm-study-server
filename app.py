
import time

from flask import Flask, jsonify, request
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


@app.route('/schools', methods=['GET'])
def schools():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    radius = request.args.get('radius', type=int)

    # Check if values are valid
    if lat is None or lon is None or radius is None:
        return jsonify({'error': 'Invalid parameters'}), 500

    return finder.find_schools(lat=lat, lon=lon, radius=radius)
