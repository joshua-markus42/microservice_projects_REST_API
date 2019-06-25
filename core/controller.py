from flask import jsonify, request
from flask_restful import Resource
import datetime
import uuid

from core.utils.schemas import ProjectSchema, DataSchema
from core.models import Projects, Data
from core import db

project_schema = ProjectSchema()
data_schema = DataSchema()


# /api/projects
class ProjectsInitializer(Resource):
    def post(self):
        data = project_schema.load(request.json)[0]
        project_name = data['name']
        contract_id = data['contract_id']
        new_project = Projects(name=project_name, contract_id=contract_id, status='waiting_for_data')
        db.session.add(new_project)
        db.session.commit()
        return jsonify({'status': 'ok'})


# /api/projects/<id>
class ProjectsResources(Resource):
    def get(self, id):
        project = Projects.query.filter_by(id=uuid.UUID(id)).first()
        return jsonify(dict(id=id, name=project.name, contract_id=project.contract_id, status=project.name))

    # update contract_id
    def put(self, id):
        data = project_schema.load(request.json)[0]
        project_name = request.json['contract_id']
        project = Projects.query.filter_by(id=uuid.UUID(id)).first()
        project.name = project_name
        db.session.commit()
        return jsonify({'status': 'updated'})


# /api/projects/status/<id>
class StatusUpdater(Resource):
    def put(self, id):
        data = project_schema.load(request.json)[0]
        new_status = data['status']
        print(new_status)
        project = Projects.query.filter_by(id=uuid.UUID(id)).first()
        project.status = new_status
        db.session.commit()
        return 'ok', 200


# /api/projects/data/<id>
class DataHandler(Resource):
    def post(self, id):
        for data in request.json().get('data'):
            print(data)
            data_about_room = Data(
                uuid.UUID(id), data['address'], data['city'], data['square'],
                data['living_square'], data['price']['currency_value'], data['price']['currency'],
                eval(data['published_date']), data['rooms'], data['toilets']
            )
            db.session.add(data_about_room)
        db.session.commit()
        return jsonify(dict(status='write_all'))
