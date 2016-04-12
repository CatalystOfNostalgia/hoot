from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine, MetaData
from json import dumps
from server.models import multimedia
from server.models import comments


#create engine to connect to SQLite
#engine_comments = create_engine('sqlite:///server/models/comments.py')
engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
app = Flask(__name__)
api = Api(app)

app = Flask(__name__)
api = Api(app)
class Multimedia(Resource):
    def get(self, media_input):
        return jsonify(param1=media_input)

api.add_resource(Multimedia, '/media/<string:media_input>')
# @app.route('/')
# class Multimedia(Resource):
#     def get(self, multimedia_name_input):
#         dumps()
#         conn = engine_multimedia.connect()
#         query = conn.execute("select * from multimedia where title ='%s'"%multimedia_name_input)
#         #perform query
#         return {'media': [i[0] for i in query.cursor.fetchall()]}
# class Comment(Resource):
#     def get(self, item_id_input):
#         dumps()
#         conn = engine_comments.connect()
#         query = conn.execute("select comment_id from comments where item_id = '%s'"%item_id_input)
#         result = {'comments': [i[0] for i in query.cursor.fetchall()]}
#         print("found result")
#         return result
#
# api.add_resource(Multimedia, '/media/<string:multimedia_name_input>')
# api.add_resource(Comment, '/media/<string:multimedia_id_input>/<string:item_id_input>')


if __name__ == '__main__':
    app.run(debug=True)