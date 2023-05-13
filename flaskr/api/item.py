from flask import Blueprint

bp = Blueprint('item', __name__, url_prefix='/item')

@bp.route('/')
def index():
    return 'Item index page'