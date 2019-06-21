from flask_restful import Api
from flask import Blueprint

from core.controller import ProjectsDataHandler, ProjectCRUD

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

api.add_resource(ProjectsDataHandler, '/projects/<id>')
api.add_resource(ProjectCRUD, '/projects')
