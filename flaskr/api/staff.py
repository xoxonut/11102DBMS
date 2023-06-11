from flask import Blueprint, jsonify, request
from flaskr.db import get_db
import datetime

bp = Blueprint("staff", __name__, url_prefix="/staff")


@bp.route("/", methods=["GET"])
def get_staff():
    db = get_db()
    cursor = db.execute("SELECT * FROM STAFF")
    staff_members = cursor.fetchall()

    staff_list = []
    for staff_member in staff_members:
        manager_id = staff_member['manager_id']
        name = staff_member['name']
        entry_date = staff_member['entry_date']
        staff = {
            "name": name,
            "manager_id": manager_id,
            "entry_date": entry_date
        }
        staff_list.append(staff)

    db.close()

    return jsonify({"staff_list": staff_list})


@bp.route("/", methods=["POST"])
def create_staff():
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        staff_data = request.json
        entry_date = datetime.datetime.now().strftime("%c")

        db = get_db()
        cursor = db.execute(
            "INSERT INTO staff (manager_id, name, entry_date) VALUES (?, ?, ?)",
            (
                staff_data.get("manager_id"),
                staff_data.get("name"),
                entry_date
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


@bp.route("/", methods=["PUT"])
def update_staff_member():
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        staff_id = request.json.get("staff_id")
        name = request.json.get("name")
        manager_id = request.json.get("manager_id")

        db = get_db()
        db.execute(
            "UPDATE STAFF SET manager_id = ?, name = ? WHERE rowid = ?",
            [manager_id, name, staff_id],
        )
        db.commit()
        db.close()

        return jsonify({"message": "Staff member updated successfully!"})

    else:
        return jsonify({"message": "Content-Type not supported!"})


@bp.route("/", methods=["DELETE"])
def delete_staff_member():
    staff_id = request.json.get("staff_id")
    db = get_db()
    cursor = db.execute("SELECT COUNT(*) AS result FROM STAFF WHERE rowid=?", [staff_id])
    rows = cursor.fetchall()
    if (rows[0]['result'] != 1):
      return {"message": "This staff doesn't exist!"}
    
    db = get_db()
    db.execute(
        "DELETE FROM staff WHERE rowid = ?",
        [staff_id],
    )
    db.commit()
    db.close()

    return jsonify({"message": "Staff member deleted successfully!"})
