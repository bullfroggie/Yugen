from flask import request, jsonify, json, Blueprint
import dateutil.parser

from utils.db import mysql, pymysql

flights = Blueprint("flights", __name__)


@flights.route("/airlines", methods=["GET"])
def get_airlines():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM airlines ORDER BY name ASC")

    airlines = cursor.fetchall()
    cursor.close()

    return jsonify(airlines), 200


@flights.route("/flight/types", methods=["GET"])
def get_flight_types():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM flight_types")

    flight_types = cursor.fetchall()
    cursor.close()

    return jsonify(flight_types), 200


@flights.route("/flights", methods=["GET"])
def get_all_flights():
    cursor = mysql.get_db().cursor()
    cursor.execute(
        "SELECT * FROM flights INNER JOIN airlines ON flights.airlines_id = airlines.id INNER JOIN flight_types ON flights.flight_types_id = flight_types.id INNER JOIN cities AS origin ON flights.origin = origin.id INNER JOIN cities AS destination ON flights.destination = destination.id INNER JOIN airports AS source_airport ON flights.source_airport = source_airport.id INNER JOIN airports AS dest_airport ON flights.destination_airport = dest_airport.id INNER JOIN flight_classes ON flights.flight_classes_id = flight_classes.id ORDER BY flights.id DESC"
    )

    flights = cursor.fetchall()
    cursor.close()

    return jsonify(flights), 200


@flights.route("/flights/search/<string:from_city>/<string:to_city>", methods=["GET"])
def search_for_flights(from_city, to_city):
    cursor = mysql.get_db().cursor()
    cursor.execute(
        "SELECT * FROM flights INNER JOIN airlines ON flights.airlines_id = airlines.id INNER JOIN flight_types ON flights.flight_types_id = flight_types.id INNER JOIN cities AS origin ON flights.origin = origin.id INNER JOIN cities AS destination ON flights.destination = destination.id INNER JOIN airports AS source_airport ON flights.source_airport = source_airport.id INNER JOIN airports AS dest_airport ON flights.destination_airport = dest_airport.id INNER JOIN flight_classes ON flights.flight_classes_id = flight_classes.id WHERE origin.name = %s AND destination.name = %s ORDER BY flights.id DESC",
        (from_city, to_city,),
    )

    flights = cursor.fetchall()
    cursor.close()

    return jsonify(flights), 200


@flights.route("/flight/classes", methods=["GET"])
def get_flight_classes():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM flight_classes")

    flight_classes = cursor.fetchall()
    cursor.close()

    return jsonify(flight_classes), 200


@flights.route("/airports", methods=["GET"])
def get_airports():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM airports ORDER BY name ASC")

    airports = cursor.fetchall()
    cursor.close()

    return jsonify(airports), 200


@flights.route("/flights", methods=["POST"])
def add_flight():
    db = mysql.get_db()
    cursor = db.cursor()

    dt = dateutil.parser.parse(request.json["flight_datetime"])
    request.json["flight_datetime"] = str(f"{dt.date()} {dt.time()}")

    cursor.execute(
        "INSERT INTO flights(airlines_id, flight_types_id, flight_classes_id, origin, destination, source_airport, destination_airport, aprox_duration, ticket_price, seats_available, flight_datetime) VALUES(%(airlines_id)s, %(flight_types_id)s, %(flight_classes_id)s, %(origin)s, %(destination)s, %(source_airport)s, %(destination_airport)s, %(aprox_duration)s, %(ticket_price)s, %(seats_available)s, %(flight_datetime)s)",
        request.json,
    )

    db.commit()
    cursor.close()

    return jsonify(request.json), 201


@flights.route("/flights/<int:flight_id>", methods=["GET"])
def get_flight(flight_id):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM flights WHERE id = %s", (flight_id,))

    flight = cursor.fetchone()
    flight["flight_datetime"] = flight["flight_datetime"].isoformat() + ".000Z"

    return jsonify(flight)


@flights.route("/flights/edit/<int:flight_id>", methods=["PUT"])
def edit_flight(flight_id):
    db = mysql.get_db()
    cursor = db.cursor()

    request.json["id"] = flight_id
    dt = dateutil.parser.parse(request.json["flight_datetime"])
    request.json["flight_datetime"] = str(f"{dt.date()} {dt.time()}")

    cursor.execute(
        "UPDATE flights SET airlines_id = %(airlines_id)s, flight_types_id = %(flight_types_id)s, flight_classes_id = %(flight_classes_id)s, origin = %(origin)s, destination = %(destination)s, source_airport = %(source_airport)s, destination_airport = %(destination_airport)s, aprox_duration = %(aprox_duration)s, ticket_price = %(ticket_price)s, seats_available = %(seats_available)s, flight_datetime = %(flight_datetime)s WHERE id = %(id)s",
        request.json,
    )
    db.commit()

    return "", 200


@flights.route("/flights/<int:flight_id>", methods=["DELETE"])
def delete_flight(flight_id):
    db = mysql.get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM flights WHERE id = %s", (flight_id,))
        db.commit()
    except pymysql.err.IntegrityError:
        return "Unable to delete this flight.", 409
    finally:
        cursor.close()

    return "", 204
