from flask import Flask, request, json, jsonify, make_response
from flask_bcrypt import Bcrypt
from flaskext.mysql import MySQL, pymysql
from datetime import datetime, timedelta
from os import urandom
import dateutil.parser
import jwt

app = Flask(__name__, static_url_path="")

app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "toor"
app.config["MYSQL_DATABASE_DB"] = "yugen_db"
app.config["SECRET_KEY"] = urandom(24)

mysql = MySQL(app, cursorclass=pymysql.cursors.DictCursor)

bcrypt = Bcrypt(app)


@app.route("/")
@app.route("/index")
def index_page():
    return app.send_static_file("index.html")


@app.route("/api/user/registration", methods=["POST"])
def user_registration():

    if "yugen_user" in request.cookies:
        return "Already logged in!", 200

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
            "This e-mail address has already been registered! Try logging in instead.",
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
            "INSERT INTO users(user_types_id, first_name, last_name, username, password, date_of_birth, email, profile_image, active) VALUES(%(user_type)s, %(first_name)s, %(last_name)s, %(username)s, %(password)s, %(date_of_birth)s, %(email)s, %(profile_image)s, %(active)s)",
            request.json,
        )
        db.commit()

        cursor.close()
        return jsonify(request.json), 201
    else:
        cursor.close()
        return "That username is taken. Try another one.", 409


@app.route("/api/user/login", methods=["POST"])
def user_login():

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
                "picture": user["profile_image"],
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

            return resp
        else:
            cursor.close()
            return "Invalid password! Please try again.", 401
    else:
        cursor.close()
        return "The email that you've entered does not match our records.", 404


@app.route("/api/user/logout", methods=["POST"])
def user_logout():
    resp = make_response("User logged out!", 205)
    resp.set_cookie("yugen_user", "", 0)

    return resp


@app.route("/api/user", methods=["GET"])
def get_logged_in():
    token = request.cookies.get("yugen_user")
    token_val = jwt.decode(token, app.config.get("SECRET_KEY"))

    if token_val:
        cursor = mysql.get_db().cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (token_val["sub"],))
        user = cursor.fetchone()

    cursor.close()

    return jsonify(user), 200


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, threaded=True)
