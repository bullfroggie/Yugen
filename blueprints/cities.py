from flask import jsonify, Blueprint

from utils.db import mysql

cities = Blueprint("cities", __name__)


@cities.route("/cities", methods=["GET"])
def get_cities():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM cities ORDER BY name ASC")

    cities = cursor.fetchall()
    cursor.close()

    return jsonify(cities), 200


@cities.route("/cities/filter/<int:country_id>", methods=["GET"])
def get_cities_by_country(country_id):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM cities WHERE countries_id = %s", (country_id,))

    cities = cursor.fetchall()
    cursor.close()

    return jsonify(cities), 200
