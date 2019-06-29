from flask import jsonify, request, abort, redirect, url_for, render_template
from flask_restful import Resource
import uuid
import logging as log

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
        log.debug("POST method")
        for data in request.json().get('data'):
            data_about_room = Data(
                uuid.UUID(id), data['address'], data['city'], data['square'],
                data['living_square'], data['price']['currency_value'], data['price']['currency'],
                eval(data['published_date']), data['rooms'], data['toilets']
            )
            db.session.add(data_about_room)
        db.session.commit()
        return {"msg": "OK"}, 200
        # return jsonify(dict(status='write_all'))


# /projects/calc/<id>
class ProjectsCalcData(Resource):

    def get(self, id):

        """
        Method to fetch data of the particular project for calculation
        :param id: an id of the project
        """
        log.debug("GET method")
        _project = Projects.query.filter_by(id=uuid.UUID(id)).first()
        if not _project:
            # abort(404)
            return {"message": "There is no such project"}, 404

        _id = str(_project.id)
        _data = Data.query.filter_by(id=uuid.UUID(_id))
        if not _data:
            abort(400)
            return {"message": "No input data provided"}, 400
        _project.status = "calculation"
        db.session.commit()
        output_prj = project_schema.dump(_project).data
        output_data = data_schema.dump(_data).data
        return jsonify({"project": output_prj, "data": output_data})

    def post(self, id):
        """
        Method to retrieve  calculated data of the particular project
        :param id: an id of the project
        """
        log.debug("POST method")

        # deserialize input json
        entry_data = request.get_json()
        if not entry_data:
            return {"message": "No input data provided"}, 400
        result = entry_data["result"]
        return {"result": result}, 200
        # # _project = Projects.query.filter_by(id=uuid.UUID(id)).first()
        # # if not _project:
        # #     return abort(jsonify(message="There is no such project"), 404)
        #     # return jsonify({"msg": "There are no such project"})
        # result = entry_data["result"]
        # if not result:
        #     return abort(jsonify(message="No input data provided"), 400)
        # return render_template('main.html', result=result)
        # return redirect(url_for('/', result=result))
            # {"msg": "Result printed"}, 200



# /api/calc/status/<id>
class ProjectsCalcStatus(Resource):
    def put(self, id):
        """
        Method to update project status data which are in calculation progress
        :param id: an id of the project
        """
        log.debug("PUT method")
        # json_data = request.get_json()

        # deserialize input json
        json_data = project_schema.load(request.json)[0]
        if not json_data:
            return abort(jsonify(message="No input data provided"), 400)

            # return jsonify({"message": "No input data provided"}), 400
        new_status = json_data["status"]

        log.debug(new_status)
        project = Projects.query.filter_by(id=uuid.UUID(id)).first()
        if not project:
            return abort(jsonify(message="There is no such project"), 404)
            # return jsonify({"msg": "Can't update - no such project"})
        project.status = new_status
        db.session.commit()
        return {"msg": "Status succefully updated"}, 200

        # result = project_schema.dump(project)
        # return project_schema.jsonify(result)
