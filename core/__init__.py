import os
from flask import Flask
# from flask.ext.session import Session
from flask_sqlalchemy import SQLAlchemy


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

db = SQLAlchemy()

from core.api import api_blueprint, api
from main.view import main


def create_app():
    app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'))
    # sess = Session()

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://e:password@localhost/flask_api'
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(main, url_prefix='/')

    with app.app_context():
        db.init_app(app)
        # sess.init_app(app)
    return app
