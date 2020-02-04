from flask import jsonify, Blueprint

from utils.db import mysql

countries = Blueprint("countries", __name__)


@countries.route("/api/countries", methods=["GET"])
def get_countries():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM countries")

    countries = cursor.fetchall()
    cursor.close()

    return jsonify(countries), 200
