import time

from flasgger import Swagger
from flask import Flask, jsonify, request
from modules.attribute_finder import LocationAttributeFinder

app = Flask(__name__)
swagger = Swagger(app)
finder = LocationAttributeFinder()


@app.route('/')
def index():
    """
    A simple index endpoint
    ---
    tags:
      - Index
    responses:
      200:
        description: Returns a simple hello world message
    """
    return 'Hello, World!'


@app.route('/ping')
def get_current_time():
    """
    A simple ping endpoint
    ---
    tags:
      - Ping
    responses:
      200:
        description: Returns the current server time
    """
    return {'pong': time.time()}


@app.route('/status')
def get_load_status():
    """
    Get load status
    ---
    tags:
      - Status
    responses:
      200:
        description: Returns the load status
    """
    return finder.get_load_status()


@app.route('/schools', methods=['GET'])
def schools():
    """
    Get schools
    ---
    tags:
      - Schools
    parameters:
      - name: lat
        in: query
        type: number
        required: true
        description: The latitude
      - name: lon
        in: query
        type: number
        required: true
        description: The longitude
      - name: radius
        in: query
        type: integer
        required: true
        description: The radius
    responses:
      200:
        description: Returns the schools within the given radius of the given latitude and longitude
      500:
        description: Invalid parameters
    """
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    radius = request.args.get('radius', type=int)

    # Check if values are valid
    if lat is None or lon is None or radius is None:
        return jsonify({'error': 'Invalid parameters'}), 500

    return finder.find_schools(lat=lat, lon=lon, radius=radius)


if __name__ == "__main__":
    app.run(debug=False)
