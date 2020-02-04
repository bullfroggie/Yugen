from flask import Flask
from os import urandom

from utils.db import mysql

from blueprints.auth import auth, bcrypt
from blueprints.users import users
from blueprints.countries import countries
from blueprints.cities import cities
from blueprints.accommodation import accommodation
from blueprints.reservations import reservations
from blueprints.flights import flights
from blueprints.flight_tickets import flight_tickets


app = Flask(__name__, static_url_path="")


app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "toor"
app.config["MYSQL_DATABASE_DB"] = "yugen_db"
app.config["SECRET_KEY"] = urandom(24)
app.config["IMAGE_UPLOADS"] = "static/styles/images/accommodation_images/"

mysql.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(users)
app.register_blueprint(countries)
app.register_blueprint(cities)
app.register_blueprint(accommodation)
app.register_blueprint(reservations)
app.register_blueprint(flights)
app.register_blueprint(flight_tickets)


@app.route("/")
@app.route("/index")
def index_page():
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, threaded=True)
