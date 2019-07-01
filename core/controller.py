from flask import jsonify, request, abort
from flask_restful import Resource
import uuid
import logging as log

from .utils.schemas import ProjectSchema, DataSchema
from .models import Projects, Data, db
from .utils.session import session

project_schema = ProjectSchema()
data_schema = DataSchema()


def get_paginated_list(klass, url, start, limit):
    # check if page exists
    results = klass.query.all()
    count = len(results)
    if (count < start):
        abort(404)
    # make response
    obj = {}
    obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count
    # make URLs
    # make previous url
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
    # make next url
    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
    # finally extract result according to bounds
    obj['results'] = results[(start - 1):(start - 1 + limit)]
    return obj


# /api/projects
class ProjectsInitializer(Resource):
    def get(self):
        # projects = Projects.query.all()
        return jsonify(get_paginated_list(
                Projects,
                '/projects',
                start=request.args.get('start', 1),
                limit=request.args.get('limit', 5)
            ))
        # return jsonify({'data': project_schema.dump(projects, many=True).data})

    def post(self):
        data = project_schema.load(request.json)[0]

        project_name = data['name']
        contract_id = data['contract_id']
        new_project = Projects(name=project_name, contract_id=contract_id, status='waiting_for_data')

        with session() as db:
            db.add(new_project)

        return jsonify({'status': 'ok'})


# /api/projects/<id>
class ProjectsResources(Resource):
    def get(self, id):
        project = Projects.query.filter_by(id=id).first()

        return jsonify(dict(id=id, name=project.name, contract_id=project.contract_id, status=project.name))

    # update contract_id
    def put(self, id):
        data = project_schema.load(request.json, partial=('contract_id',))[0]

        contract_id = data['contract_id']
        project = Projects.query.filter_by(id=id).first()
        project.contract_id = contract_id
        db.session.commit()

        return jsonify({'status': 'updated'})


# /api/projects/status/<id>
class StatusUpdater(Resource):
    def put(self, id):
        data = project_schema.load(request.json, partial=('status',))[0]

        new_status = data['status']
        project = Projects.query.filter_by(id=id).first()
        project.status = new_status
        db.session.commit()

        return jsonify({'status': 'updated'})


# /api/projects/data/<id>
class DataHandler(Resource):
    def post(self, id):
        data = data_schema.load(request.json)[0]

        for data in data['data']:
            data_about_room = Data(
                project_id=uuid.UUID(id),
                address=data['address'],
                city=data['city'],
                square=data['square'],
                living_square=data['living_square'],
                currency_value=data['price']['currency_value'],
                currency=data['price']['currency'],
                published_date=data['published_date'],
                rooms=data['rooms'],
                toilets=data['toilets']
            )
            db.session.add(data_about_room)
        db.session.commit()

        return jsonify({'status': 'write_all'})


# /projects/<id>/calc
class ProjectsCalc(Resource):

    def get(self, id):

        """
        Method to fetch data of the particular project for calculation
        :param id: an id of the project
        """
        log.debug("GET method")
        _project = Projects.query.filter_by(id=uuid.UUID(id)).first()
        if not _project:
            abort(404)
            return {"message": "There is no such project"}, 404

        _id = str(_project.id)
        _data = Data.query.filter_by(id=uuid.UUID(_id))
        if not _data:
            abort(400)
            return {"message": "No input data provided"}, 400
        if not bool(_data):
            abort(400)
            return {"message": "Empty data"}, 400
        _project.status = "calculation"
        db.session.commit()
        try:
            output_prj = project_schema.dump(_project).data
            output_data = data_schema.dump(_data).data
        except:
            abort(400)
            return {"message": "Something is wrong"}, 400
        return jsonify({"project": output_prj, "data": output_data}), 200

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


# /api/calc/status/<id>
class ProjectsCalcResult(Resource):
    def put(self, id):
        """
        Method to update project status data which are in calculation progress
        :param id: an id of the project
        """
        log.debug("PUT method")

        # deserialize input json
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400

        new_status = json_data["status"]

        project = Projects.query.filter_by(id=uuid.UUID(id)).first()
        if not project:
            return {"message": "Can't update - no such project"}, 404

        try:
            project.status = new_status
            db.session.commit()
        except:
            return {"message": "Wrong"}, 418
        return {"message": "Status succefully updated for {}".format(new_status)}, 200
