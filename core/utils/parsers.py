from flask import request
from flask_restful import reqparse


def status_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('status', type=str)
    data = parser.parse_args()
    return data


def data_parser():
    print(request.get_json())
    parser = reqparse.RequestParser()
    # print()
    parser.add_argument('address', action='append')
    data = parser.parse_args()
    # print(data)
    return data
