from flask import Blueprint

bp = Blueprint('purchase_order', __name__, url_prefix='/purchase_order')

@bp.route('/')
def index():
    return 'Purchase Order index page'