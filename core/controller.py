from flask import jsonify, request
from flask_restful import Resource
import datetime
import uuid

from .models import Projects, Data
from . import db


class Project(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass


class ProjectsCollector(Resource):

    def put(self, id):
        new_status = request.json["status"]
        project = Projects.query.filter_by(id=uuid.UUID(id)).first()
        project.status = new_status
        db.session.commit()
        return jsonify(dict(id=project.id, status=project.status))

    def get(self, id):
        pass

    def post(self, id):
        for data in request.json:
            data_about_room = Data(
                uuid.UUID(id), data['address'], data['city'], data['square'],
                data['living_square'], data['price']['currency_value'], data['price']['currency'],
                eval(data['published_date']), data['rooms'], data['toilets']
            )
            db.session.add(data_about_room)
        db.session.commit()
        return jsonify(dict(status='write_all'))

    def delete(self, id):
        db.session.query(Data).filter(Data.project_id == uuid.UUID(id)).delete()
        db.session.commit()
        return jsonify(dict(status='delete'))
