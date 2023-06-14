from flask import Blueprint, jsonify, request
from flaskr.db import get_db

bp = Blueprint("item", __name__, url_prefix="/item")


@bp.route("/", methods=["GET"])
def read_item():
    db = get_db()

    cursor = db.execute("SELECT * FROM ITEM")
    rows = cursor.fetchall()

    item_list = []
    for row in rows:
        item_id = row['item_id']
        name = row['name']
        type = row['type']
        stock = row['stock']
        unit_price = row['unit_price'] 
        item = {
            "id": item_id,
            "name": name,
            "type": type,
            "stock": stock,
            "unit_price": unit_price
        }
        item_list.append(item)

    db.close()

    return jsonify({"item_list": item_list})


@bp.route("/", methods=["PUT"])
def update_item():
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        item_id = request.json.get("item_id")
        unit_price = request.json.get("unit_price")

        if item_id is None or unit_price is None:
            return jsonify({"error": "Missing item_id or unit_price"})

        db = get_db()
        db.execute(
          "UPDATE ITEM SET unit_price = ? WHERE rowid = ?", [unit_price, item_id]
        )
        db.commit()

        db.close()

        return jsonify({"message": "Item updated successfully"})

    return jsonify({"error": "Invalid Content-Type"})

@bp.route("/<item_id>", methods=["GET"])
def get_item_supplier(item_id):
    db = get_db()
    try:
        cursor = db.execute(
            "SELECT DISTINCT SUPPLIER.supplier_id, SUPPLIER.name\
                FROM ITEM,SUPPLIER,INCREASE,PURCHASE_ORDER\
                WHERE ITEM.item_id = ?\
                    AND ITEM.item_id = INCREASE.item_id\
                    AND INCREASE.p_order_id = PURCHASE_ORDER.p_order_id\
                    AND PURCHASE_ORDER.supplier_id = SUPPLIER.supplier_id",
            item_id
        )
        rows = cursor.fetchall()
        supplier_list = []
        for row in rows:
            supplier = {
                "supplier_id": row["supplier_id"],
                "name": row["name"]
            }
            supplier_list.append(supplier)
    except:
        return jsonify({"error": "Item not found"})
    finally:
        db.close()
    return jsonify({"supplier_list": supplier_list})