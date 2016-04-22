#!/usr/bin/env python
import rdflib

from flask import Flask
from flask_restful import Resource, Api, reqparse

from emotion_processing import comment_emotions
from search.searcher import search

app = Flask(__name__)
api = Api(app)


class MultimediaAPI(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('product', type=str)
        parser.add_argument('emotion', type=str)
        args = parser.parse_args()
        return search(args['product'], args['emotion'])


class EmotionAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        args = parser.parse_args()
        print("THIS IS WORKING!")

        f = open('senticnet3.rdf.xml')
        g = rdflib.Graph()
        g.parse(f)

        emotion = comment_emotions.emotions(args['text'], g)
        sentic_values = emotion.get_all_sentic_values()
        compound_emotions = emotion.get_compound_emotion()

        sentic_values = [e.name for e in sentic_values if e is not None]
        compound_emotions = [(e.name, v.name) for e, v in compound_emotions]

        return {
            'sentic_values': sentic_values,
            'compound_emotions': compound_emotions
        }


@app.route('/', methods=['GET'])
def index():
    return 'You are being greeted by hoot!'

api.add_resource(MultimediaAPI, '/search', endpoint='search')
api.add_resource(EmotionAPI, '/emotions', endpoint='emotions')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
