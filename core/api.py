from flask import Blueprint
from flask_restful import Api

from core.controller import Home, ProjectCRUD, ProjectsDataHandler, ProjectsCalc

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

api.add_resource(Home, '/')
api.add_resource(ProjectCRUD, '/projects/<id>')
api.add_resource(ProjectsDataHandler, '/projects/data/<id>')
api.add_resource(ProjectsCalc, '/projects/calc/<id>')
