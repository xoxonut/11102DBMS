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
        staff_id = staff_member['staff_id']
        manager_id = staff_member['manager_id']
        name = staff_member['name']
        entry_date = staff_member['entry_date']
        staff = {
            "staff_id": staff_id,
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
    try:
        if content_type == "application/json":
            staff_data = request.json
            entry_date = datetime.datetime.now().strftime("%c")
            db = get_db()
            cursor = db.execute('Select staff_id from staff')
            staff_ids = cursor.fetchall()
            if staff_data.get('manager_id')!='' and int(staff_data.get('manager_id')) not in [x['staff_id'] for x in staff_ids]:
                return {"message": "This manager doesn't exist!"}
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
    except Exception as e:
        return jsonify({"message": str(e)})


@bp.route("/", methods=["PUT"])
def update_staff_member():
    try:
        content_type = request.headers.get("Content-Type")
        if content_type == "application/json":
            staff_id = request.json.get("staff_id")
            name = request.json.get("name")
            manager_id = request.json.get("manager_id")
            print(staff_id,name,manager_id)
            db = get_db()
            cursor = db.execute('Select staff_id from staff')
            staff_ids = cursor.fetchall()
            if manager_id !='' and int(manager_id) not in [x['staff_id'] for x in staff_ids]:
                return {"message": "This manager doesn't exist!"}

            db.execute(
                "UPDATE STAFF SET manager_id = ?, name = ? WHERE rowid = ?",
                [manager_id, name, staff_id],
            )
            db.commit()
            db.close()

            return jsonify({"message": "Staff member updated successfully!"})

        else:
            return jsonify({"message": "Content-Type not supported!"})
    except Exception as e:
        return jsonify({"message": str(e)})


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
    
    db.execute("UPDATE STAFF SET manager_id = '' WHERE manager_id = ?", [staff_id])
    db.commit()
    db.close()
    return jsonify({"message": "Staff member deleted successfully!"})
