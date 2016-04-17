#!/usr/bin/env python
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

@app.route('/', methods=['GET'])
def index():
    return 'You are being greeted by hoot!'

class MultimediaAPI(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('product', type=str)
        parser.add_argument('emotion', type=str)

        return parser.parse_args()

api.add_resource(MultimediaAPI, '/search', endpoint='search')

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=80)
    app.run(debug=True)
