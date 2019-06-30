from .config import create_app
from .api import api_blueprint, api
from .controller import DataHandler, ProjectsInitializer, ProjectsResources, StatusUpdater
from .controller import ProjectsCalc, ProjectsCalcResult

app = create_app()
app.register_blueprint(api_blueprint)

api.add_resource(ProjectsInitializer, '/projects')
api.add_resource(ProjectsResources, '/projects/<id>')

api.add_resource(DataHandler, '/projects/<id>/data')
api.add_resource(StatusUpdater, '/projects/<id>/status')

api.add_resource(ProjectsCalc, '/projects/<id>/calc')
api.add_resource(ProjectsCalcResult, '/projects/<id>/result')
