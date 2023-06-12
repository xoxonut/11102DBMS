from flask import Blueprint, jsonify, request
from flaskr.db import get_db

bp = Blueprint("supplier", __name__, url_prefix="/supplier")


@bp.route("/", methods=["GET"])
def get_suppliers():
    db = get_db()
    cursor = db.execute("SELECT * FROM SUPPLIER")
    suppliers = cursor.fetchall()
    supplier_list = []
    for supplier in suppliers:
        name = supplier['name']
        email = supplier['email']
        phone_number = supplier['phone_number']
        address = supplier['address']
        one_supplier = {
            "name": name,
            "email": email,
            "phone":phone_number,
            "address": address
        }
        supplier_list.append(one_supplier)

    db.close()

    return jsonify({"supplier_list": supplier_list})


@bp.route("/", methods=["POST"])
def create_supplier():
    print(request.headers)
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        supplier_data = request.json
        db = get_db()
        cursor = db.execute(
            "INSERT INTO supplier (name,email, phone_number,address) VALUES (?, ?, ?, ?)",
            (
                supplier_data.get("name"),
                supplier_data.get("email"),
                supplier_data.get("phone_number"),
                supplier_data.get("address")
            ),
        )
        supplier_id = cursor.lastrowid
        db.commit()
        db.close()

        return jsonify(
            {"message": "Supplier created successfully!", "supplier_id": supplier_id}
        )

    else:
        return jsonify({"message": "Content-Type not supported!"})

@bp.route("/", methods=["PUT"])
def update_supplier():
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        supplier_id = request.json.get("supplier_id")
        name = request.json.get("name")
        email = request.json.get("email")
        phone_number = request.json.get("phone_number")
        address = request.json.get("address")

        db = get_db()
        db.execute(
            "UPDATE SUPPLIER SET name= ?,email = ?,phone_number = ?,address = ? WHERE rowid = ?",
            [ name,email,phone_number,address, supplier_id],
        )
        db.commit()
        db.close()

        return jsonify({"message": "Staff member updated successfully!"})

    else:
        return jsonify({"message": "Content-Type not supported!"})
    
@bp.route("/", methods=["DELETE"])
def delete_supplier():
     supplier_id = request.json.get("supplier_id")
     db = get_db()
     cursor = db.execute("SELECT COUNT(*) AS result FROM SUPPLIER WHERE rowid=?", [supplier_id])
     rows = cursor.fetchall()
     if (rows[0]['result'] != 1):
      return {"message": "This supplier doesn't exist!"}
     db = get_db()
     db.execute("DELETE FROM SUPPLIER WHERE rowid=?", [supplier_id])
     db.commit()
     db.close()
     return jsonify({"message": "Supplier deleted successfully"})
