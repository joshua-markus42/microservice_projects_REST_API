from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from .api import api_blueprint, api
from config import DATABASE_URI

moment = Moment()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    api.init_app(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://arthur:arthur234@localhost/projects'
    app.register_blueprint(api_blueprint)
    with app.app_context():
        db.init_app(app)

    return app
