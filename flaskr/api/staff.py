from flask import Blueprint

bp = Blueprint('staff', __name__, url_prefix='/staff')

@bp.route('/')
def index():
    return 'Staff index page'