from flask_restful import Api
from flask import Blueprint

from core.resources import ProjectsCollector

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

api.add_resource(ProjectsCollector, '/<id>')
