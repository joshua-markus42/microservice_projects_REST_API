from flask import Blueprint, request
from flask import render_template

main = Blueprint('main', __name__)


@main.route('/', methods=["GET", "POST"])
def home():
    return render_template('main.html')
