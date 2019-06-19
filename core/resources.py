from flask import jsonify
from flask_restful import Resource


class ProjectsCollector(Resource):
    def put(self, id):
        return jsonify(id)