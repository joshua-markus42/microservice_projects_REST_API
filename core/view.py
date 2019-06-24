from flask import Blueprint
# from . import app
import logging as login
from flask import render_template

bp = Blueprint('main', __name__)


@app.route('/', methods=["GET"])
def home():
    login.debug("Get method")
    return render_template('main.html')
