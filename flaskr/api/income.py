from flask import Blueprint, jsonify, request
from flaskr.db import get_db

bp = Blueprint("income", __name__, url_prefix="/income")

@bp.route("/", methods=["GET"])
def read_income():
  content_type = request.headers.get('Content-Type')
  if (content_type == 'application/json'):
    month = request.json.get('month')
    year = request.json.get('year')
    db = get_db()
    cursor = db.execute("""
        SELECT D.item_quantity, I.unit_price
        FROM SALES_ORDER S, DECREASE D, ITEM I
        WHERE S.s_order_date LIKE ? AND S.s_order_id = D.s_order_id AND D.item_id = I.item_id""", ('%'+month+'%'+year,))
    rows = cursor.fetchall()

    # calculate total_income in the month
    total_income = 0
    for row in rows:
      item_quantity = row['item_quantity']
      unit_price = row['unit_price']
      total_income = total_income + (item_quantity*unit_price)
      print("quantity: "+str(item_quantity)+" unit_price: "+str(unit_price)+" sum: "+str(total_income))

    db.close()
    return jsonify({"income": total_income})
  else:
    return jsonify({"message": "Content-Type not supported!"})