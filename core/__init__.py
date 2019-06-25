from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .api import api_blueprint, api


def create_app():
    app = Flask(__name__)
    api.init_app(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://arthur:arthur234@localhost/projects'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_blueprint(api_blueprint, url_prefix='/api')

    with app.app_context():
        db.init_app(app)

    return app
