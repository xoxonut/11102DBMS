from flask import Blueprint, jsonify, request
from flaskr.db import get_db

bp = Blueprint("staff_performance", __name__, url_prefix="/staff_performance")

@bp.route("/", methods=["GET"])
def read_performance():
  content_type = request.headers.get('Content-Type')
  if (content_type == 'application/json'):
    month = request.json.get('month')
    year = request.json.get('year')
    db = get_db()
    # TODO: add time parameter
    cursor = db.execute("""
        SELECT SUM(D.item_quantity * I.unit_price) AS performance, ST.name
        FROM SALES_ORDER S, DECREASE D, ITEM I, STAFF ST
        WHERE S.s_order_date LIKE ? AND S.s_order_id = D.s_order_id AND D.item_id = I.item_id AND ST.staff_id = S.staff_id
        GROUP BY ST.staff_id""", ('%'+month+'%'+year,))
    rows = cursor.fetchall()

    staff_list = []
    for row in rows:
      staff = {
        "name": row['name'],
        "performance": row['performance']
      }
      staff_list.append(staff)

    db.close()
    return jsonify({"performance_list": staff_list})
  else:
    return jsonify({"message": "Content-Type not supported!"})
