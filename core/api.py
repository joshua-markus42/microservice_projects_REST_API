from flask_restful import Api
from flask import Blueprint

from core.controller import ProjectsDataHandler, ProjectsInitializer, ProjectsResources

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

api.add_resource(ProjectsDataHandler, '/projects/data/<id>')
api.add_resource(ProjectsInitializer, '/projects')
api.add_resource(ProjectsResources, '/projects/<id>')
# api.add_resource(ProjectCRUD, '/projects')
