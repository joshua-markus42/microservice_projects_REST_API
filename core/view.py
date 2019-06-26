from flask import Blueprint
from flask import render_template

main = Blueprint('main', __name__)


@main.route('/', methods=["GET"])
def home():
    return render_template('main.html')
