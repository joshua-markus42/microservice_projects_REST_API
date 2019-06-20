from flask import jsonify
from flask_restful import Resource

from . import db


class ProjectsCollector(Resource):
    def put(self, id):
        return jsonify(id)
# class ProjectsCollector(Resource):
#     pass
# #     def put(self, id):
# #         status = request.json["status"]
# #         projects = Projects.query().filter_by(id=id).first()
# #         projects.status = status
# #         db.session.commit()
# #         return jsonify('Ok')
