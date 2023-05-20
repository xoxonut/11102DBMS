from flask import Blueprint, jsonify
from flaskr.db import get_db

bp = Blueprint("item", __name__, url_prefix="/item")


@bp.route("/item")
def index():
    db = get_db()

    cursor = db.execute("SELECT * FROM ITEM")
    rows = cursor.fetchall()

    item_list = []
    for row in rows:
        item_id, name, type, stock, unit_price = row
        item_list.append([item_id, name, type, stock, unit_price])

    return jsonify(item_list)
