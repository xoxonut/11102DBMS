from flask import Blueprint,jsonify

bp = Blueprint('staff', __name__, url_prefix='/staff')

@bp.route('/')
def index():
    ret = [{'name':'test','code':1}]
    return jsonify(ret)