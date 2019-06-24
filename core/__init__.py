from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

from .api import api_blueprint, api
from .view import bp


def create_app():
    app = Flask(__name__, template_folder='templates')
    api.init_app(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://e:password@localhost/flask_api'
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(bp.bp, url_prefix='/')

    with app.app_context():
        db.init_app(app)
        ma.init_app(app)

    return app
