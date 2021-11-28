import threading
import json
from wsgiref.simple_server import WSGIRequestHandler
import requests
from flask import Flask, jsonify, request
from requests.exceptions import ConnectionError

app_data = {}

MOCK_RECONNECT_LIMIT = 5

app = Flask(__name__)
WSGIRequestHandler.protocol_version = "HTTP/1.1"


@app.route('/create_user', methods=['POST'])
def create_user():
    name = json.loads(request.data)['name']
    phone = json.loads(request.data)['phone_number']

    if app_data.get(name) is None:
        app_data[name] = phone
        data = {'name': name, 'phone_number': phone}
        return jsonify(data), 201
    else:
        return jsonify(f'User with name {name} already exists.'), 400


@app.route('/get_phone/<name>', methods=['GET'])
def get_user_phone_number(name):
    if phone := app_data.get(name):
        data = {'name': name, 'phone_number': phone}
        return jsonify(data), 200
    else:
        return jsonify(f'User with name {name} does not exist.'), 404


@app.route('/change_phone', methods=['PUT'])
def change_user_phone_number():
    name = json.loads(request.data)['name']
    if app_data.get(name) is not None:
        new_number = json.loads(request.data)['new_phone']
        app_data[name] = new_number
        data = {'name': name, 'phone_number': new_number}
        return jsonify(data), 201
    else:
        return jsonify(f'User with name {name} does not exist.'), 404


@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    name = json.loads(request.data)['name']
    if app_data.get(name) is not None:
        app_data.pop(name)
        return jsonify(f'User {name} was deleted successfully!'), 200
    else:
        return jsonify(f'User with name {name} does not exist.'), 404


def run_mock(host, port):
    server = threading.Thread(target=app.run, kwargs={
        'host': host,
        'port': port
    })
    server.start()

    for i in range(MOCK_RECONNECT_LIMIT):
        try:
            requests.get(f'http://{host}:{port}')
            break
        except ConnectionError:
            if i == MOCK_RECONNECT_LIMIT - 1:
                raise

    return server


@app.route('/shutdown')
def shutdown_mock():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()
    return jsonify(f'Exit done successfully.'), 200
