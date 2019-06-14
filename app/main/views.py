from . import main


@main.route('/', methods=['GET','POST'])
def index():
    return 'Projects API 1.0'