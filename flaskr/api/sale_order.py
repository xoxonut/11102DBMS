from flask import Blueprint

bp = Blueprint('sale_order', __name__, url_prefix='/sale_order')

@bp.route('/')
def index():
    return 'Sale Order index page'