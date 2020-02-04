from flask import request, json, jsonify, Blueprint, current_app
import os
import shutil

from utils.db import mysql

accommodation = Blueprint("accommodation", __name__)


@accommodation.route("/api/accommodation/types", methods=["GET"])
def get_accommodation_types():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM accommodation_types")

    accommodation_types = cursor.fetchall()
    cursor.close()

    return jsonify(accommodation_types), 200


@accommodation.route("/api/accommodation", methods=["GET"])
def get_all_accommodations():
    cursor = mysql.get_db().cursor()
    cursor.execute(
        "SELECT * FROM accommodation INNER JOIN cities ON accommodation.cities_id = cities.id INNER JOIN accommodation_types ON accommodation.accommodation_types_id = accommodation_types.id ORDER BY accommodation.name ASC"
    )

    accommodations = cursor.fetchall()
    cursor.close()

    return jsonify(accommodations), 200


@accommodation.route("/api/accommodation", methods=["POST"])
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


@accommodation.route("/api/accommodation/upload/<hotel>", methods=["POST"])
def upload_images(hotel):

    app = current_app._get_current_object()

    os.mkdir(os.path.join(app.config["IMAGE_UPLOADS"], hotel))
    images = request.files.to_dict()
    for image in images:
        images[image].save(
            os.path.join(app.config["IMAGE_UPLOADS"], hotel, images[image].filename)
        )

    return "", 201


@accommodation.route("/api/accommodation/images", methods=["GET"])
def get_images():

    app = current_app._get_current_object()

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


@accommodation.route("/api/accommodation/<int:accommodation_id>", methods=["GET"])
def get_accommodation(accommodation_id):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM accommodation WHERE id = %s", (accommodation_id,))

    accommodation = cursor.fetchone()

    return jsonify(accommodation), 200


@accommodation.route("/api/accommodation/city/<city_name>", methods=["GET"])
def get_accommodation_by_city(city_name):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM cities WHERE name = %s", (city_name,))
    city = cursor.fetchone()

    if city is None:
        return "Not Found", 404

    cursor.execute(
        "SELECT * FROM accommodation WHERE cities_id = %s ORDER BY name ASC",
        (city["id"],),
    )

    accommodations = cursor.fetchall()
    cursor.close()

    return jsonify(accommodations), 200


@accommodation.route("/api/accommodation/details/<int:id>", methods=["GET"])
def get_accommodation_by_id(id):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM accommodation WHERE id = %s", (id,))

    accommodation = cursor.fetchone()
    cursor.close()

    return jsonify(accommodation), 200


@accommodation.route(
    "/api/accommodation/filter/<string:city_name>/<int:stars>", methods=["GET"]
)
def filter_accommodation_by_stars(city_name, stars):
    cursor = mysql.get_db().cursor()

    cursor.execute("SELECT * FROM cities WHERE name = %s", (city_name,))
    city = cursor.fetchone()

    if city is None:
        return "Not Found", 404

    cursor.execute(
        "SELECT * FROM accommodation WHERE cities_id = %s AND stars = %s AND available > 0",
        (city["id"], stars,),
    )

    filtered = cursor.fetchall()
    cursor.close()

    return jsonify(filtered), 200


@accommodation.route("/api/accommodation/edit/<int:accommodation_id>", methods=["PUT"])
def edit_accommodation(accommodation_id):

    app = current_app._get_current_object()

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


@accommodation.route("/api/accommodation/<int:accommodation_id>", methods=["DELETE"])
def delete_accommodation(accommodation_id):

    app = current_app._get_current_object()

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
