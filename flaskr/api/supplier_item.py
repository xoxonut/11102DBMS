from flask import Blueprint, jsonify, request
from flaskr.db import get_db

bp = Blueprint("supplier_item", __name__, url_prefix="/supplier_item")

@bp.route("/", methods=["POST"])
def read_supplier_items():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        supplier_name = request.json.get('name')

        db = get_db()
        cursor = db.execute("""
            SELECT DISTINCT I.item_id, I.name, I.type, I.stock, I.unit_price
            FROM ITEM I
            JOIN INCREASE INC ON I.item_id = INC.item_id
            JOIN PURCHASE_ORDER PO ON INC.p_order_id = PO.p_order_id
            JOIN SUPPLIER S ON PO.supplier_id = S.supplier_id
            WHERE S.name = ?""", (supplier_name,))
        rows = cursor.fetchall()
        db.close()

        supplier_items = []
        for row in rows:
            item = {
                'item_id': row['item_id'],
                'name': row['name'],
                'type': row['type'],
                'stock': row['stock'],
                'unit_price': row['unit_price']
            }
            supplier_items.append(item)

        return jsonify({"supplier_items": supplier_items})
    else:
        return jsonify({"message": "Content-Type not supported!"})

