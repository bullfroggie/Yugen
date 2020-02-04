from flask import request, jsonify, json, Blueprint

from utils.db import mysql

flight_tickets = Blueprint("flight_tickets", __name__)


@flight_tickets.route("/api/flights/ticket", methods=["POST"])
def purchase_ticket():
    db = mysql.get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO flight_tickets(flights_id, users_id) VALUES(%(flights_id)s, %(users_id)s)",
        request.json,
    )
    cursor.execute(
        "UPDATE flights SET seats_available = seats_available - 1 WHERE id = %s",
        (request.json["flights_id"],),
    )
    db.commit()
    cursor.close()

    return jsonify(request.json), 201


@flight_tickets.route("/api/tickets/<int:id>", methods=["GET"])
def get_tickets(id):
    cursor = mysql.get_db().cursor()
    cursor.execute(
        "SELECT * FROM flight_tickets INNER JOIN flights ON flight_tickets.flights_id = flights.id INNER JOIN airlines ON flights.airlines_id = airlines.id INNER JOIN flight_types ON flights.flight_types_id = flight_types.id INNER JOIN cities AS origin ON flights.origin = origin.id INNER JOIN cities AS destination ON flights.destination = destination.id INNER JOIN airports AS source_airport ON flights.source_airport = source_airport.id INNER JOIN airports AS dest_airport ON flights.destination_airport = dest_airport.id INNER JOIN flight_classes ON flights.flight_classes_id = flight_classes.id WHERE users_id = %s",
        (id,),
    )

    tickets = cursor.fetchall()
    cursor.close()

    return jsonify(tickets), 200


@flight_tickets.route(
    "/api/tickets/<int:flight_id>/<int:ticket_id>", methods=["DELETE"]
)
def delete_ticket(flight_id, ticket_id):
    db = mysql.get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM flight_tickets WHERE id = %s", (ticket_id,))
    cursor.execute(
        "UPDATE flights SET seats_available = seats_available + 1 WHERE id = %s",
        (flight_id,),
    )
    db.commit()
    cursor.close()

    return "", 204
