from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

from .api import api_blueprint, api


DBUSER = 'postgres'
DBPASS = ''
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'postgres'

db = SQLAlchemy()
migrate = Migrate()


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def postgres_uri():
    return 'postgresql://e:password@localhost/flask_api'


def create_app():
    app = Flask(__name__)
    api.init_app(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = postgres_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)

    return app
