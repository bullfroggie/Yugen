from flask import request, json, jsonify, make_response, Blueprint, current_app
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import dateutil.parser
import jwt

from utils.db import mysql

auth = Blueprint("auth", __name__)

bcrypt = Bcrypt()


@auth.route("/api/user/registration", methods=["POST"])
def user_registration():

    db = mysql.get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE email = %(email)s", request.json)
    checked_user = cursor.fetchone()

    if checked_user is None:
        cursor.execute(
            "SELECT * FROM users WHERE username = %(username)s", request.json
        )
        checked_user = cursor.fetchone()
    else:
        cursor.close()
        return (
            "This e-mail address has already been registered!",
            409,
        )

    if checked_user is None:
        request.json["password"] = bcrypt.generate_password_hash(
            request.json["password"]
        ).decode("utf-8")

        """
        Convert date from ISO 8601 to yyyy-dd-mm
        """
        dt = dateutil.parser.parse(request.json["date_of_birth"])
        request.json["date_of_birth"] = str(dt.date())

        cursor.execute(
            "INSERT INTO users(user_types_id, first_name, last_name, username, password, date_of_birth, email) VALUES(%(user_type)s, %(first_name)s, %(last_name)s, %(username)s, %(password)s, %(date_of_birth)s, %(email)s)",
            request.json,
        )
        db.commit()

        cursor.close()
        return jsonify(request.json), 201
    else:
        cursor.close()
        return "That username is taken. Try another one.", 409


@auth.route("/api/user/login", methods=["POST"])
def user_login():

    app = current_app._get_current_object()

    cursor = mysql.get_db().cursor()
    cursor.execute(
        "SELECT * FROM users WHERE email = %(email)s", request.json,
    )

    user = cursor.fetchone()

    if user is not None:

        if bcrypt.check_password_hash(user["password"], request.json["password"]):
            payload = {
                "exp": datetime.utcnow() + timedelta(days=90),
                "iat": datetime.utcnow(),
                "type": user["user_types_id"],
                "name": f"{user['first_name']} {user['last_name']}",
                "sub": user["id"],
            }

            resp = make_response("User authentication successful!", 200)
            resp.set_cookie(
                "yugen_user",
                jwt.encode(payload, app.config.get("SECRET_KEY"), algorithm="HS256"),
                expires=datetime.utcnow() + timedelta(days=90),
            )

            cursor.close()
            return resp
        else:
            cursor.close()
            return "Invalid password! Please try again.", 401
    else:
        cursor.close()
        return "The email that you've entered does not match our records.", 404


@auth.route("/api/user/logout", methods=["POST"])
def user_logout():
    resp = make_response("User logged out!", 205)
    resp.set_cookie("yugen_user", "", 0)

    return resp
