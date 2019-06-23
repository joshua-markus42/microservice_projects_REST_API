from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

from core.api import api_blueprint, api


def create_app():
    app = Flask(__name__)
    api.init_app(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://e:password@localhost/flask_api'
    app.register_blueprint(api_blueprint, url_prefix='/')

    with app.app_context():
        db.init_app(app)
        ma.init_app(app)

    return app
