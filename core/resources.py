from flask import jsonify, request
from flask_restful import Resource
import uuid

from .models import Projects
from . import db


class ProjectsCollector(Resource):

    def put(self, id):
        new_status = request.json["status"]

        project = Projects.query.filter_by(id=uuid.UUID(id)).first()
        project.status = new_status
        db.session.commit()
        return jsonify(dict(id=project.id, status=project.status))

