from flask import Blueprint

bp = Blueprint('member', __name__, url_prefix='/member')

@bp.route('/')
def index():
    return 'Member index page'