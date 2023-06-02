from flask import Blueprint, jsonify, request
from flaskr.db import get_db

bp = Blueprint("staff", __name__, url_prefix="/myErp/staff")


@bp.route("/", methods=["GET"])
def get_staff():
    db = get_db()
    cursor = db.execute("SELECT * FROM staff")
    staff_members = cursor.fetchall()
    db.close()

    staff_list = []
    for staff_member in staff_members:
        staff_dict = {
            "staff_id": staff_member["staff_id"],
            "manager_id": staff_member["manager_id"],
            "name": staff_member["name"],
            "entry_date": staff_member["entry_date"],
        }
        staff_list.append(staff_dict)

    return jsonify({"staff_members": staff_list})


@bp.route("/", methods=["POST"])
def create_staff():
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        staff_data = request.json

        db = get_db()
        cursor = db.execute(
            "INSERT INTO staff (manager_id, name, entry_date) VALUES (?, ?, ?)",
            (
                staff_data.get("manager_id"),
                staff_data.get("name"),
                staff_data.get("entry_date"),
            ),
        )
        staff_id = cursor.lastrowid
        db.commit()
        db.close()

        return jsonify(
            {"message": "Staff member created successfully!", "staff_id": staff_id}
        )

    else:
        return jsonify({"message": "Content-Type not supported!"})


@bp.route("/<int:staff_id>", methods=["GET"])
def get_staff_member(staff_id):
    db = get_db()
    cursor = db.execute("SELECT * FROM staff WHERE staff_id = ?", (staff_id,))
    staff_member = cursor.fetchone()
    db.close()

    if staff_member is None:
        return jsonify({"message": "Staff member not found!"}), 404

    staff_dict = {
        "staff_id": staff_member["staff_id"],
        "manager_id": staff_member["manager_id"],
        "name": staff_member["name"],
        "entry_date": staff_member["entry_date"],
    }

    return jsonify(staff_dict)


@bp.route("/<int:staff_id>", methods=["PUT"])
def update_staff_member(staff_id):
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        staff_data = request.json

        db = get_db()
        cursor = db.execute(
            "UPDATE staff SET manager_id = ?, name = ?, entry_date = ? WHERE staff_id = ?",
            (
                staff_data.get("manager_id"),
                staff_data.get("name"),
                staff_data.get("entry_date"),
                staff_id,
            ),
        )
        db.commit()
        db.close()

        return jsonify({"message": "Staff member updated successfully!"})

    else:
        return jsonify({"message": "Content-Type not supported!"})


@bp.route("/<int:staff_id>", methods=["DELETE"])
def delete_staff_member(staff_id):
    db = get_db()
    cursor = db.execute("DELETE FROM staff WHERE staff_id = ?", (staff_id,))
    db.commit()
    db.close()

    return jsonify({"message": "Staff member deleted successfully!"})
