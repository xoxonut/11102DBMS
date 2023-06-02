from flask import Blueprint, jsonify, request
from flaskr.db import get_db
import datetime
import random

bp = Blueprint("supplier", __name__, url_prefix="/supplier")


@bp.route("/", methods=["GET"])
def read_suppliers():
    db = get_db()
    cursor = db.execute(
        """
        SELECT S.rowid AS supplier_id, S.staff_id, S.name AS supplier_name, S.entry_date, ST.name AS staff_name
        FROM SUPPLIER S
        LEFT JOIN STAFF ST ON S.staff_id = ST.rowid
    """
    )
    rows = cursor.fetchall()

    supplier_list = []
    for row in rows:
        supplier_id, staff_id, supplier_name, entry_date, staff_name = row
        supplier = {
            "supplier_id": supplier_id,
            "staff_id": staff_id,
            "supplier_name": supplier_name,
            "entry_date": entry_date,
            "staff_name": staff_name,
        }
        supplier_list.append(supplier)

    db.close()

    return jsonify(supplier_list)


@bp.route("/", methods=["POST"])
def create_supplier():
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        staff_id = request.json.get("staff_id")
        name = request.json.get("name")
        entry_date = request.json.get("entry_date")

        db = get_db()

        # Check if the staff exists
        cursor = db.execute(
            "SELECT COUNT(*) AS result FROM STAFF WHERE rowid=?", [staff_id]
        )
        rows = cursor.fetchall()
        if rows[0]["result"] != 1:
            return jsonify({"message": "This staff doesn't exist!"})

        # Insert into the supplier table
        supplier_id = random.randint(1000, 100000)
        cursor = db.execute(
            "INSERT INTO SUPPLIER (supplier_id, staff_id, name, entry_date) VALUES (?, ?, ?, ?)",
            [supplier_id, staff_id, name, entry_date],
        )
        db.commit()

        return jsonify({"message": "Supplier created successfully"})
    else:
        return jsonify({"message": "Content-Type not supported!"})


@bp.route("/<int:supplier_id>", methods=["GET"])
def get_supplier(supplier_id):
    db = get_db()
    cursor = db.execute(
        """
        SELECT S.rowid AS supplier_id, S.staff_id, S.name AS supplier_name, S.entry_date, ST.name AS staff_name
        FROM SUPPLIER S
        LEFT JOIN STAFF ST ON S.staff_id = ST.rowid
        WHERE S.rowid = ?
    """,
        [supplier_id],
    )
    supplier = cursor.fetchone()

    if supplier is None:
        return jsonify({"message": "Supplier not found"})

    supplier_id, staff_id, supplier_name, entry_date, staff_name = supplier
    supplier_data = {
        "supplier_id": supplier_id,
        "staff_id": staff_id,
        "supplier_name": supplier_name,
        "entry_date": entry_date,
        "staff_name": staff_name,
    }

    return jsonify(supplier_data)


@bp.route("/<int:supplier_id>", methods=["PUT"])
def update_supplier(supplier_id):
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        staff_id = request.json.get("staff_id")
        name = request.json.get("name")
        entry_date = request.json.get("entry_date")

        db = get_db()

        # Check if the supplier exists
        cursor = db.execute(
            "SELECT COUNT(*) AS result FROM SUPPLIER WHERE rowid=?", [supplier_id]
        )
        rows = cursor.fetchall()
        if rows[0]["result"] != 1:
            return jsonify({"message": "Supplier not found"})

        # Check if the staff exists
        cursor = db.execute(
            "SELECT COUNT(*) AS result FROM STAFF WHERE rowid=?", [staff_id]
        )
        rows = cursor.fetchall()
        if rows[0]["result"] != 1:
            return jsonify({"message": "This staff doesn't exist!"})

        # Update the supplier
        db.execute(
            "UPDATE SUPPLIER SET staff_id = ?, name = ?, entry_date = ? WHERE rowid = ?",
            [staff_id, name, entry_date, supplier_id],
        )
        db.commit()

        return jsonify({"message": "Supplier updated successfully"})
    else:
        return jsonify({"message": "Content-Type not supported!"})


@bp.route("/<int:supplier_id>", methods=["DELETE"])
def delete_supplier(supplier_id):
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        db = get_db()

        # Check if the supplier exists
        cursor = db.execute(
            "SELECT COUNT(*) AS result FROM SUPPLIER WHERE rowid=?", [supplier_id]
        )
        rows = cursor.fetchall()
        if rows[0]["result"] != 1:
            return jsonify({"message": "Supplier not found"})

        # Delete the supplier
        db.execute("DELETE FROM SUPPLIER WHERE rowid=?", [supplier_id])
        db.commit()

        return jsonify({"message": "Supplier deleted successfully"})
    else:
        return jsonify({"message": "Content-Type not supported!"})
