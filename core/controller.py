import logging as login
import uuid

from flask import jsonify, request, render_template
from flask_restful import Resource

from . import db
from core.models import Projects, Data, project_schema, data_schema


# class Home(Resource):
#
#     def get(self):
#         login.debug("Get method")
#         return render_template('main.html')
#         # return {"msg": "GET method. "}, 200
#
#     def post(self):
#         login.debug("Get method")
#         # return render_template('login.html', error=error)
#         return {"msg": "POST method. "}, 200


class ProjectCRUD(Resource):
    """
    Manipulate with particular project
    """

    def get(self):
        """
        Method to get all project data by id
        """
        login.debug("Get method")
        # project_id = request.json['id']
        # project = Projects.query.filter_by(id=uuid.UUID(project_id)).first()
        # return jsonify(dict(name=project.name, status=project.name))
        return {"msg": "GET method of projects"}, 200

    def post(self):
        """
        Method to add a new project into the database
        """
        # new_project_name = request.json['id']
        # new_project = Projects(str(new_project_name), 'waiting_for_data')
        # db.session.add(new_project)
        # db.session.commit()
        # return jsonify('Successfully added')

    def delete(self):
        """
        Method to delete a project
        """
        project_id = request.json['id']
        db.session.query(Projects).filter(Projects.id == uuid.UUID(project_id)).delete()
        db.session.commit()
        return jsonify('Successfully deleted')

    def put(self):
        """
        Method to change the name of a project
        """
        project_id = request.json['id']
        project_name = request.json['name']
        project = Projects.query.filter_by(id=uuid.UUID(project_id)).first()
        project.name = project_name
        db.session.commit()
        return jsonify('Successfully updated')


class ProjectsDataHandler(Resource):
    """
    Manipulate the project data
    """

    def put(self, id):
        """
        Method to update project status when uploading data
        :param id: an id of the project
        """
        new_status = request.json["status"]
        project = Projects.query.filter_by(id=uuid.UUID(id)).first()
        project.status = new_status
        db.session.commit()
        return jsonify(dict(id=project.id, status=project.status))

    def post(self, id):
        """
        Method to write data in database
        :param id: an id of the project
        """
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
        """
        Method to delete all data of the particular project
        :param id: an id of the project
        """
        db.session.query(Data).filter(Data.project_id == uuid.UUID(id)).delete()
        db.session.commit()
        return jsonify(dict(status='delete'))

    def get(self, id):
        """
        Method to get all data of the particular project
        :param id: an id of the project
        """
        pass


class ProjectsCalc(Resource):

    # def get(self, id):

    # """
    #         Method to fetch data of the particular project for calculation
    #         :param id: an id of the project
    #         """
    #         project = Projects.query.get(id)
    #         output = project_schema.dump(project).data
    #         return project_schema.jsonify({'project': output})

    def post(self, id):
        """
        Method to post data of the particular project for calculation
        :param id: an id of the project
        """
        # entry_data = request.get_json()
        # _id = entry_data['id']
        _project = Projects.query.filter_by(id=uuid.UUID(id)).first_or_404()
        _data = Data.query.filter_by(id=uuid.UUID(_project.id)).first_or_404()
        _project.status = "calculation"
        db.session.commit()
        output_prj = project_schema.dump(_project).data
        output_data = data_schema.dump(_data).data
        return project_schema.jsonify({'project': output_prj, 'data': output_data})

    def put(self, id):
        """
        Method to update project status data are in calculation progress
        :param id: an id of the project
        """
        login.debug("PUT method")
        # entry_data = request.get_json()
        # _id = entry_data['id']
        project = Projects.query.filter_by(id=uuid.UUID(id)).first()
        if not project:
            return jsonify({"msg": "Can't update - no such project"})
        new_status = request.json["status"]
        project.status = new_status
        db.session.commit()
        return {"msg": "Put method of projects"}, 200
        # result = project_schema.dump(project)
        # return project_schema.jsonify(result)
