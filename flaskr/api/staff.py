from flask import Blueprint, jsonify, request
from flaskr.db import get_db

bp = Blueprint("staff", __name__, url_prefix="/staff")


@bp.route("/get_staff", methods=["GET"])
def get_staff():
    db = get_db()
    cursor = db.execute("SELECT * FROM STAFF")
    staff_members = cursor.fetchall()

    staff_list = []
    for staff_member in staff_members:
        manager_id, name, entry_date = staff_member
        staff_list.append([manager_id, name, entry_date])

    db.close()

    return jsonify(staff_list)


@bp.route("/create_staff", methods=["POST"])
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


@bp.route("/update_staff_member", methods=["PUT"])
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


@bp.route("/delete_staff_member", methods=["DELETE"])
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
