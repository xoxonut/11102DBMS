from flask import Blueprint, jsonify
from flaskr.db import get_db

bp = Blueprint('purchase_order', __name__, url_prefix='/purchase_order')

@bp.route('/', methods=['GET'])
def read_purchase_order():
  db = get_db()
  cursor = db.execute("""
      SELECT p_order_id, SP.name AS supplier_name, ST.name AS staff_name, p_order_date
      FROM PURCHASE_ORDER P, SUPPLIER SP, STAFF ST
      WHERE P.supplier_id = SP.supplier_id AND P.staff_id = ST.staff_id""")
  rows = cursor.fetchall()

  item_list=[]
  for row in rows:
    p_order_id, supplier_name,  staff_name, p_order_date = row
    item = {
      "p_order_id": p_order_id,
      "supplier_name": supplier_name,
      "staff_name": staff_name,
      "p_order_date": p_order_date
    }
    item_list.append(item)
  
  return jsonify({"p_order_list": item_list})
  