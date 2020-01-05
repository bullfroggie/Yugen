from flask import Flask, request, json, jsonify
from flask_bcrypt import Bcrypt
from flaskext.mysql import MySQL, pymysql
import dateutil.parser

app = Flask(__name__, static_url_path="")

app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "toor"
app.config["MYSQL_DATABASE_DB"] = "yugen_db"

mysql = MySQL(app, cursorclass=pymysql.cursors.DictCursor)

bcrypt = Bcrypt(app)


@app.route("/")
@app.route("/index")
def index_page():
    return app.send_static_file("index.html")


@app.route("/api/user/registration", methods=["POST"])
def user_registration():
    db = mysql.get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE username = %(username)s", request.json)
    checked_username = cursor.fetchone()

    if checked_username is None:
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
        return "", 409


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, threaded=True)
