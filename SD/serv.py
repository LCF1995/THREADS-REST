from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('type')
parser.add_argument('text')

class TodoList(Resource):

    def post(self):
        args = parser.parse_args()
        if args['type'] == 'concate':
        	res = {'text' : args['text'].replace(" ", ""), 'type': 'concate'}
        	return res, 201
        elif args['type'] == 'upper':
        	res = {'text' : args['text'].upper(), 'type': 'upper'}
        	return res , 201

        return args, 201

api.add_resource(TodoList, '/')

if __name__ == '__main__':
    app.run(debug=True)