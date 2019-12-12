from flask import Flask, jsonify
from flaskext.mysql import MySQL, pymysql

app = Flask(__name__, static_url_path="")

app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "toor"
app.config["MYSQL_DATABASE_DB"] = "yugen_db"

mysql = MySQL(app, cursorclass = pymysql.cursors.DictCursor)

@app.route("/")
@app.route("/index")
def index_page():
    return app.send_static_file("index.html")

@app.route("/api/users", methods=["GET"])
def get_users():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    
    return jsonify(users)

@app.route("/api/accommodation", methods=["GET"])
def get_accommodation():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM accommodation")
    accommodation = cursor.fetchall()

    return jsonify(accommodation)








if __name__ == "__main__":
    app.run("0.0.0.0", 5000, threaded=True)