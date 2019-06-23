from flask import Flask
from flask_restful import Resource, Api
from requests import put

app = Flask(__name__)
api = Api(app)

route = 'http://127.0.0.1:5000/projects/6a2cb5b8-fc2d-45ef-ba40-a651eb65e21a'


class HelloWorld(Resource):
    def get(self):
        put(route, data={'status': 'hello'}).json()
        return 'ok'


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=6000)
