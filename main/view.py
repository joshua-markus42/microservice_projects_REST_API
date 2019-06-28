import os
from flask import Blueprint, request, Flask, flash, redirect
from flask import render_template
# from flask.e
    # flaskext.uploads import UploadSet, configure_uploads, DATA
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

UPLOAD_FOLDER = 'main/uploads'

# data = UploadSet('data', DATA)
# configure_uploads(main, data)


# main.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = set(['txt', 'csv'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/', methods=["GET", "POST"])
def home():
    return render_template('main.html')

#
# @main.route('/upload')
# def upload_file():
#     return render_template('load.html')
#
#
# @main.route('/', methods=['POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         if file.filename == '':
#             flash('No file selected for uploading')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(UPLOAD_FOLDER, filename))
#             flash('File successfully uploaded')
#             return redirect('/')
#         else:
#             flash('Allowed file types are txt, csv')
#             return redirect(request.url)
