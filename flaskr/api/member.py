from flask import Blueprint, jsonify, request, render_template
from flaskr.db import get_db
from random import randint

bp = Blueprint("member", __name__, url_prefix="/member")


@bp.route("/get_members", methods=["GET"])
def get_members():
    db = get_db()
    cursor = db.execute("SELECT * FROM member")
    members = cursor.fetchall()
    db.close()

    member_list = []
    for member in members:
        member_dict = {
            "member_id": member["member_id"],
            "name": member["name"],
            "address": member["address"],
            "email": member["email"],
            "phone_number": member["phone_number"],
        }
        member_list.append(member_dict)

    return jsonify({"members": member_list})


@bp.route("/create_member", methods=["POST"])
def create_member():
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        member_data = request.json

        db = get_db()
        cursor = db.execute(
            "INSERT INTO member (name, address, email, phone_number) VALUES (?, ?, ?, ?)",
            (
                member_data.get("name"),
                member_data.get("address"),
                member_data.get("email"),
                member_data.get("phone_number"),
            ),
        )
        member_id = cursor.lastrowid
        db.commit()
        db.close()

        return jsonify(
            {"message": "Member created successfully!", "member_id": member_id}
        )

    else:
        return jsonify({"message": "Content-Type not supported!"})


@bp.route("/get_member", methods=["GET"])
def get_member(member_id):
    db = get_db()
    cursor = db.execute("SELECT * FROM member WHERE member_id = ?", (member_id,))
    member = cursor.fetchone()
    db.close()

    if member is None:
        return jsonify({"message": "Member not found!"}), 404

    member_dict = {
        "member_id": member["member_id"],
        "name": member["name"],
        "address": member["address"],
        "email": member["email"],
        "phone_number": member["phone_number"],
    }

    return jsonify(member_dict)


@bp.route("/update_member", methods=["PUT"])
def update_member(member_id):
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        member_data = request.json

        db = get_db()
        cursor = db.execute("SELECT * FROM member WHERE member_id = ?", (member_id,))
        member = cursor.fetchone()

        if member is None:
            return jsonify({"message": "Member not found!"}), 404

        cursor = db.execute(
            "UPDATE member SET name = ?, address = ?, email = ?, phone_number = ? WHERE member_id = ?",
            (
                member_data.get("name"),
                member_data.get("address"),
                member_data.get("email"),
                member_data.get("phone_number"),
                member_id,
            ),
        )
        db.commit()
        db.close()

        return jsonify({"message": "Member updated successfully!"})

    else:
        return jsonify({"message": "Content-Type not supported!"})


@bp.route("/delete_member", methods=["DELETE"])
def delete_member(member_id):
    db = get_db()
    cursor = db.execute("DELETE FROM member WHERE member_id = ?", (member_id,))
    db.commit()
    db.close()

    return jsonify({"message": "Member deleted successfully!"})
