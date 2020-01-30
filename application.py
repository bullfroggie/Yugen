from flask import Flask, request, json, jsonify, make_response
from flask_bcrypt import Bcrypt
from flaskext.mysql import MySQL, pymysql
from datetime import datetime, timedelta
import os
import shutil
import dateutil.parser
import jwt

app = Flask(__name__, static_url_path="")

app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "toor"
app.config["MYSQL_DATABASE_DB"] = "yugen_db"
app.config["SECRET_KEY"] = os.urandom(24)
app.config["IMAGE_UPLOADS"] = "static/styles/images/accommodation_images/"

mysql = MySQL(app, cursorclass=pymysql.cursors.DictCursor)

bcrypt = Bcrypt(app)


@app.route("/test", methods=["POST"])
def upload_test():

    return "", 201


@app.route("/")
@app.route("/index")
def index_page():
    return app.send_static_file("index.html")


@app.route("/api/user/registration", methods=["POST"])
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
            "INSERT INTO users(user_types_id, first_name, last_name, username, password, date_of_birth, email, profile_image) VALUES(%(user_type)s, %(first_name)s, %(last_name)s, %(username)s, %(password)s, %(date_of_birth)s, %(email)s, %(profile_image)s)",
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

            cursor.close()
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


@app.route("/api/users", methods=["GET"])
def get_all_users():
    token = request.cookies.get("yugen_user")
    token_val = jwt.decode(token, app.config.get("SECRET_KEY"))

    cursor = mysql.get_db().cursor()
    cursor.execute(
        "SELECT * FROM users WHERE id != %s ORDER BY id DESC", (token_val["sub"],)
    )

    users = cursor.fetchall()
    cursor.close()

    return jsonify(users), 200


@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    db.commit()
    cursor.close()

    return "", 204


@app.route("/api/cities", methods=["GET"])
def get_cities():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM cities ORDER BY name ASC")

    cities = cursor.fetchall()
    cursor.close()

    return jsonify(cities), 200


@app.route("/api/accommodation/types", methods=["GET"])
def get_accommodation_types():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM accommodation_types")

    accommodation_types = cursor.fetchall()
    cursor.close()

    return jsonify(accommodation_types), 200


@app.route("/api/accommodation", methods=["GET"])
def get_all_accommodations():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM accommodation ORDER BY name ASC")

    accommodations = cursor.fetchall()
    cursor.close()

    return jsonify(accommodations), 200


@app.route("/api/accommodation", methods=["POST"])
def add_accommodation():
    db = mysql.get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM accommodation WHERE name = %(name)s", request.json)
    existing_check = cursor.fetchone()

    if existing_check is not None:
        return "Accommodation with that name already exists!", 409

    cursor.execute(
        "INSERT INTO accommodation(accommodation_types_id, cities_id, name, price_per_night, stars, street_address, description, breakfast, internet, available) VALUES(%(accommodation_types_id)s, %(cities_id)s, %(name)s, %(price_per_night)s, %(stars)s, %(street_address)s, %(description)s, %(breakfast)s, %(internet)s, %(available)s)",
        request.json,
    )

    db.commit()
    cursor.close()

    return jsonify(request.json), 201


@app.route("/api/accommodation/upload/<hotel>", methods=["POST"])
def upload_images(hotel):

    os.mkdir(os.path.join(app.config["IMAGE_UPLOADS"], hotel))
    images = request.files.to_dict()
    for image in images:
        images[image].save(
            os.path.join(app.config["IMAGE_UPLOADS"], hotel, images[image].filename)
        )

    return "", 201


@app.route("/api/accommodation/<int:accommodation_id>", methods=["GET"])
def get_accommodation(accommodation_id):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM accommodation WHERE id = %s", (accommodation_id,))

    accommodation = cursor.fetchone()

    return jsonify(accommodation), 200


@app.route("/api/accommodation/city/<int:city_id>", methods=["GET"])
def get_accommodation_by_city(city_id):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM accommodation WHERE cities_id = %s ORDER BY name ASC", (city_id,))

    accommodations = cursor.fetchall()

    return jsonify(accommodations), 200


@app.route("/api/accommodation/edit/<int:accommodation_id>", methods=["PUT"])
def edit_accommodation(accommodation_id):
    db = mysql.get_db()
    cursor = db.cursor()

    cursor.execute("SELECT name FROM accommodation WHERE id = %s", (accommodation_id,))
    prev_name = cursor.fetchone()

    # rename accommodation image directory
    os.rename(
        os.path.join(app.config["IMAGE_UPLOADS"], prev_name["name"]),
        os.path.join(app.config["IMAGE_UPLOADS"], request.json["name"]),
    )

    request.json["id"] = accommodation_id
    cursor.execute(
        "UPDATE accommodation SET accommodation_types_id = %(accommodation_types_id)s, cities_id = %(cities_id)s, name = %(name)s, price_per_night = %(price_per_night)s, stars = %(stars)s, street_address = %(street_address)s, description = %(description)s, breakfast = %(breakfast)s, internet = %(internet)s, available = %(available)s WHERE id = %(id)s",
        request.json,
    )
    db.commit()

    return "", 200


@app.route("/api/accommodation/<int:accommodation_id>", methods=["DELETE"])
def delete_accommodation(accommodation_id):
    db = mysql.get_db()
    cursor = db.cursor()

    cursor.execute("SELECT name FROM accommodation WHERE id = %s", (accommodation_id,))
    accommodation_name = cursor.fetchone()

    # removes accommodation image directory along with all of the images
    shutil.rmtree(os.path.join(app.config["IMAGE_UPLOADS"], accommodation_name["name"]))

    cursor.execute("DELETE FROM accommodation WHERE id = %s", (accommodation_id,))
    db.commit()
    cursor.close()

    return "", 204


@app.route("/api/airlines", methods=["GET"])
def get_airlines():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM airlines ORDER BY name ASC")

    airlines = cursor.fetchall()
    cursor.close()

    return jsonify(airlines), 200


@app.route("/api/flight/types", methods=["GET"])
def get_flight_types():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM flight_types")

    flight_types = cursor.fetchall()
    cursor.close()

    return jsonify(flight_types), 200


@app.route("/api/flights", methods=["GET"])
def get_all_flights():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM flights ORDER BY id DESC")

    flights = cursor.fetchall()
    cursor.close()

    return jsonify(flights), 200


@app.route("/api/flight/classes", methods=["GET"])
def get_flight_classes():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM flight_classes")

    flight_classes = cursor.fetchall()
    cursor.close()

    return jsonify(flight_classes), 200


@app.route("/api/airports", methods=["GET"])
def get_airports():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM airports ORDER BY name ASC")

    airports = cursor.fetchall()
    cursor.close()

    return jsonify(airports), 200


@app.route("/api/flights", methods=["POST"])
def add_flight():
    db = mysql.get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO flights(airlines_id, flight_types_id, flight_classes_id, origin, destination, source_airport, destination_airport, aprox_duration, ticket_price, seats_available) VALUES(%(airlines_id)s, %(flight_types_id)s, %(flight_classes_id)s, %(origin)s, %(destination)s, %(source_airport)s, %(destination_airport)s, %(aprox_duration)s, %(ticket_price)s, %(seats_available)s)",
        request.json,
    )

    db.commit()
    cursor.close()

    return jsonify(request.json), 201


@app.route("/api/flights/<int:flight_id>", methods=["GET"])
def get_flight(flight_id):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM flights WHERE id = %s", (flight_id,))

    flight = cursor.fetchone()

    return jsonify(flight)


@app.route("/api/flights/edit/<int:flight_id>", methods=["PUT"])
def edit_flight(flight_id):
    db = mysql.get_db()
    cursor = db.cursor()

    request.json["id"] = flight_id
    cursor.execute(
        "UPDATE flights SET airlines_id = %(airlines_id)s, flight_types_id = %(flight_types_id)s, flight_classes_id = %(flight_classes_id)s, origin = %(origin)s, destination = %(destination)s, source_airport = %(source_airport)s, destination_airport = %(destination_airport)s, aprox_duration = %(aprox_duration)s, ticket_price = %(ticket_price)s, seats_available = %(seats_available)s WHERE id = %(id)s",
        request.json,
    )
    db.commit()

    return "", 200


@app.route("/api/flights/<int:flight_id>", methods=["DELETE"])
def delete_flight(flight_id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM flights WHERE id = %s", (flight_id,))
    db.commit()
    cursor.close()

    return "", 204


@app.route("/api/accommodation/images", methods=["GET"])
def get_images():
    listed = []

    with os.scandir(app.config["IMAGE_UPLOADS"]) as entries:
        for entry in entries:
            if entry.is_dir():
                with os.scandir(
                    os.path.join(app.config["IMAGE_UPLOADS"], entry.name)
                ) as sub:
                    for sub_entry in sub:
                        corrected_path = sub_entry.path[7:]
                        entry_dict = {"name": entry.name, "path": corrected_path}
                        listed.append(entry_dict)

    return jsonify(listed), 200


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, threaded=True)
