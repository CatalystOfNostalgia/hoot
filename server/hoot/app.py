#!/usr/bin/env python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'You are being greeted by hoot!'

@app.route('/hoot/api/v1.0/', methods=['GET'])
def v1_index():
    return jsonify({'hello': 'Hello World!'})


if __name__ == '__main__':
        app.run(host='0.0.0.0', port=80)




