from flask import request, jsonify, json, Blueprint
import dateutil.parser

from utils.db import mysql

reservations = Blueprint("reservations", __name__)


@reservations.route("/api/accommodation/reservation", methods=["POST"])
def make_reservation():
    db = mysql.get_db()
    cursor = db.cursor()

    """
    Convert date from ISO 8601 to yyyy-dd-mm
    """
    dt = dateutil.parser.parse(request.json["date"])
    request.json["date"] = str(dt.date())

    cursor.execute(
        "INSERT INTO reservations (accommodation_id, users_id, nights, date, total_price) VALUES(%(accommodation_id)s, %(users_id)s, %(nights)s, %(date)s, %(total_price)s)",
        request.json,
    )
    cursor.execute(
        "UPDATE accommodation SET available = available - 1 WHERE id = %s",
        (request.json["accommodation_id"],),
    )
    db.commit()
    cursor.close()

    return jsonify(request.json), 201


@reservations.route("/api/reservations/<int:id>", methods=["GET"])
def get_reservations(id):
    cursor = mysql.get_db().cursor()
    cursor.execute(
        "SELECT * FROM reservations INNER JOIN accommodation ON reservations.accommodation_id = accommodation.id INNER JOIN cities ON accommodation.cities_id = cities.id INNER JOIN accommodation_types ON accommodation.accommodation_types_id = accommodation_types.id WHERE users_id = %s",
        (id,),
    )

    reservations = cursor.fetchall()
    cursor.close()

    return jsonify(reservations), 200


@reservations.route(
    "/api/reservations/<int:accommodation_id>/<int:reservation_id>", methods=["DELETE"]
)
def delete_reservation(accommodation_id, reservation_id):
    db = mysql.get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM reservations WHERE id = %s", (reservation_id,))
    cursor.execute(
        "UPDATE accommodation SET available = available + 1 WHERE id = %s",
        (accommodation_id,),
    )
    db.commit()
    cursor.close()

    return "", 204
