from flask import Blueprint
from flask_restful import Api

from core.controller import DataHandler, ProjectsInitializer, ProjectsResources, StatusUpdater
from core.controller import ProjectsCalcData, ProjectsCalcStatus


api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

api.add_resource(ProjectsInitializer, '/projects')
api.add_resource(ProjectsResources, '/projects/<id>')

api.add_resource(DataHandler, '/projects/data/<id>')
api.add_resource(StatusUpdater, '/projects/status/<id>')

api.add_resource(ProjectsCalcData, '/projects/calc/<id>')
# api.add_resource(ProjectsCalcStatus, '/calc/status/<id>')
