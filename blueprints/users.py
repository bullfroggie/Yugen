from flask import request, json, jsonify, Blueprint, current_app
import jwt

from utils.db import mysql

users = Blueprint("users", __name__)


@users.route("/api/user", methods=["GET"])
def get_logged_in():

    app = current_app._get_current_object()

    token = request.cookies.get("yugen_user")
    token_val = jwt.decode(token, app.config.get("SECRET_KEY"))

    if token_val:
        cursor = mysql.get_db().cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (token_val["sub"],))
        user = cursor.fetchone()

    cursor.close()

    return jsonify(user), 200


@users.route("/api/users", methods=["GET"])
def get_all_users():

    app = current_app._get_current_object()

    token = request.cookies.get("yugen_user")
    token_val = jwt.decode(token, app.config.get("SECRET_KEY"))

    cursor = mysql.get_db().cursor()
    cursor.execute(
        "SELECT * FROM users WHERE id != %s ORDER BY id DESC", (token_val["sub"],)
    )

    users = cursor.fetchall()
    cursor.close()

    return jsonify(users), 200


@users.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    db = mysql.get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM reservations WHERE users_id = %s", (user_id,))
    cursor.execute("DELETE FROM flight_tickets WHERE users_id = %s", (user_id,))
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    db.commit()
    cursor.close()

    return "", 204
