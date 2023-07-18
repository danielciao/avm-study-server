import os
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


@app.route('/epc', methods=['GET'])
def epc():
    """
    Get EPC Certificates
    ---
    tags:
      - EPC
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
      - name: top
        in: query
        type: integer
        required: true
        description: The top n closest matches
    responses:
      200:
        description: Returns the top n closest match of the given latitude and longitude
      500:
        description: Invalid parameters
    """
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    top_n = request.args.get('top', type=int)

    # Check if values are valid
    if lat is None or lon is None or top_n is None:
        return jsonify({'error': 'Invalid parameters'}), 500

    return finder.find_epc(lat=lat, lon=lon, top_n=top_n)


@app.route('/transports', methods=['GET'])
def transports():
    """
    Get transports
    ---
    tags:
      - Transports
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
        description: Returns the number of public transport access points within the given radius of the given latitude and longitude
      500:
        description: Invalid parameters
    """
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    radius = request.args.get('radius', type=int)

    # Check if values are valid
    if lat is None or lon is None or radius is None:
        return jsonify({'error': 'Invalid parameters'}), 500

    return finder.find_transport(lat=lat, lon=lon, radius=radius)


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


@app.route('/greenspace', methods=['GET'])
def greenspace():
    """
    Get green space
    ---
    tags:
      - Green Space
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
      - name: top
        in: query
        type: integer
        required: true
        description: The top n green spaces
    responses:
      200:
        description: Returns the top n closest match of the given latitude and longitude
      500:
        description: Invalid parameters
    """
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    top_n = request.args.get('top', type=int)

    # Check if values are valid
    if lat is None or lon is None or top_n is None:
        return jsonify({'error': 'Invalid parameters'}), 500

    return finder.find_green_space(lat=lat, lon=lon, top_n=top_n)


@app.route('/imd', methods=['GET'])
def imd():
    """
    Get IMD Decile
    ---
    tags:
      - IMD
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
      - name: top
        in: query
        type: integer
        required: true
        description: The top n closest matches
    responses:
      200:
        description: Returns the top n closest match of the given latitude and longitude
      500:
        description: Invalid parameters
    """
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    top_n = request.args.get('top', type=int)

    # Check if values are valid
    if lat is None or lon is None or top_n is None:
        return jsonify({'error': 'Invalid parameters'}), 500

    return finder.find_imd(lat=lat, lon=lon, top_n=top_n)


if __name__ == "__main__":
    app.run()
