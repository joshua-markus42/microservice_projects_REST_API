from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

db = SQLAlchemy()
# ma = Marshmallow()

from core.api import api_blueprint, api
from core.view import main


def create_app():
    app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'))
    api.init_app(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://e:password@localhost/flask_api'
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(main, url_prefix='/')

    with app.app_context():
        db.init_app(app)
        # ma.init_app(app)

    return app
