from flask import jsonify, request
from flask_restful import Resource
import datetime
import uuid

from .utils.parsers import status_parser, data_parser
from .models import Projects, Data
from . import db


class ProjectsDataHandler(Resource):
    def put(self, id):
        data = status_parser()
        new_status = data['status']
        print(new_status)
        project = Projects.query.filter_by(id=uuid.UUID(id)).first()
        project.status = new_status
        db.session.commit()
        return 'ok', 200

    def post(self, id):

        for data in request.get_json().get('data'):
            print(data)
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


class ProjectCRUD(Resource):
    def get(self):
        project_id = request.json['id']
        project = Projects.query.filter_by(id=uuid.UUID(project_id)).first()
        return jsonify(dict(name=project.name, status=project.name))

    def post(self):
        new_project_name = request.json['name']
        new_project = Projects(str(new_project_name), 'waiting_for_data')
        db.session.add(new_project)
        db.session.commit()
        return jsonify('Successfully added')

    def delete(self):
        project_id = request.json['id']
        db.session.query(Projects).filter(Projects.id == uuid.UUID(project_id)).delete()
        db.session.commit()
        return jsonify('Successfully deleted')

    def put(self):
        project_id = request.json['id']
        project_name = request.json['name']
        project = Projects.query.filter_by(id=uuid.UUID(project_id)).first()
        project.name = project_name
        db.session.commit()
        return jsonify('Successfully updated')
