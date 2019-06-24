from flask import Flask
from flask_restful import Resource, Api
from requests import put, post

app = Flask(__name__)
api = Api(app)

route_for_testing_data = 'http://127.0.0.1:5000/projects/6a2cb5b8-fc2d-45ef-ba40-a651eb65e21a'


class HelloJSON(Resource):
    def get(self):
        post(route_for_testing_data, json={
            "data": [
                {
                    "address": "P.O. Box 664, 3059 Litora Road",
                    "city": "Presteigne",
                    "square": 237.0,
                    "living_square": 161.0,
                    "rooms": 3,
                    "published_date": "datetime.datetime(2018, 8, 19, 0, 0)",
                    "price":
                        {
                            "currency_value": 14.83,
                            "currency": "USD"
                        },
                    "toilets": 3
                },
                {
                    "address": "fsdfasasdfasdf",
                    "city": "asdfasfde",
                    "square": 23.1,
                    "living_square": 1.3,
                    "rooms": 5,
                    "published_date": "datetime.datetime(2011, 8, 19, 0, 0)",
                    "price":
                        {
                            "currency_value": 1.83,
                            "currency": "RU"
                        },
                    "toilets": 0
                }
            ]})
        return 'ok'


api.add_resource(HelloJSON, '/')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=6000)
