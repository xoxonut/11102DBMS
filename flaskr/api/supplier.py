from flask import Blueprint

bp = Blueprint('supplier', __name__, url_prefix='/supplier')

@bp.route('/')
def index():
    return 'Supplier index page'