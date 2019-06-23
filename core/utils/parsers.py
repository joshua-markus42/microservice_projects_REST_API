from flask_restful import reqparse


def status_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('status', type=str)
    data = parser.parse_args()
    return data


def data_parser():
    parser = reqparse.RequestParser()

    parser.add_argument('address', type=str, location='json')
    parser.add_argument('city', type=str, location='json')
    parser.add_argument('')
