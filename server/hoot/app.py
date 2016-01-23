#!../env/bin/python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/hoot/api/v1.0/', methods=['GET'])
def index():
    return jsonify({'hello': 'Hello World!'})


if __name__ == '__main__':
    app.run(debug=True)


