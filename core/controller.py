from flask import jsonify, request
from flask_restful import Resource
import datetime
import uuid

from .models import Projects, RoomsData
from . import db


class ProjectsCollector(Resource):

    def put(self, id):
        new_status = request.json["status"]
        project = Projects.query.filter_by(id=uuid.UUID(id)).first()
        project.status = new_status
        db.session.commit()
        return jsonify(dict(id=project.id, status=project.status))

    def post(self, id):
        for data in request.json:
            data_about_room = RoomsData(
                uuid.UUID(id), data['address'], data['city'], data['square'],
                data['living_square'], data['price']['currency_value'], data['price']['currency'],
                eval(data['published_date']), data['rooms'], data['toilets']
            )
            db.session.add(data_about_room)
        db.session.commit()
        return jsonify(dict(status='write_all'))

    def delete(self, id):
        db.session.query(RoomsData).filter(RoomsData.project_id == uuid.UUID(id)).delete()
        # print(a)
        db.session.commit()
        return jsonify('delete')
