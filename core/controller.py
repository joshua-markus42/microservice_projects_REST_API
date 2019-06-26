from flask import jsonify, request
from flask_restful import Resource
import uuid
import logging as login

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


# /api/calc/data/<id>
class ProjectsCalcData(Resource):

    def get(self, id):

        """
        Method to fetch data of the particular project for calculation
        :param id: an id of the project
        """
        login.debug("GET method")
        # project = Projects.query.get(id)
        # output = project_schema.dump(project).data
        # return project_schema.jsonify({'project': output})
        # entry_data = request.get_json()

        _project = Projects.query.filter_by(id=uuid.UUID(id)).first_or_404()
        _data = Data.query.filter_by(id=uuid.UUID(_project.id)).first_or_404()
        _project.status = "calculation"
        db.session.commit()
        output_prj = project_schema.dump(_project).data
        output_data = data_schema.dump(_data).data
        return project_schema.jsonify({"project": output_prj, "data": output_data})

    def post(self, id):
        """
        Method to retrieve  calculated data of the particular project
        :param id: an id of the project
        """
        login.debug("POST method")

        # deserialize input json
        # entry_data = request.get_json() ???
        json_data = project_schema.load(request.json)[0]
        if not json_data:
            return jsonify({"message": "No input data provided"}), 400
        _project = Projects.query.filter_by(id=uuid.UUID(id)).first_or_404()
        if not _project:
            return jsonify({"msg": "There are no such project"})
        result = json_data['result']
        return {"msg": "Result printed"}, 200


# /api/calc/status/<id>
class ProjectsCalcStatus(Resource):
    def put(self, id):
        """
        Method to update project status data which are in calculation progress
        :param id: an id of the project
        """
        login.debug("PUT method")
        # json_data = request.get_json()

        # deserialize input json
        json_data = project_schema.load(request.json)[0]
        if not json_data:
            return jsonify({"message": "No input data provided"}), 400
        new_status = json_data['status']
        print(new_status)
        project = Projects.query.filter_by(id=uuid.UUID(id)).first()
        if not project:
            return jsonify({"msg": "Can't update - no such project"})
        project.status = new_status
        db.session.commit()
        return {"msg": "Status succefully updated"}, 200

        # result = project_schema.dump(project)
        # return project_schema.jsonify(result)
