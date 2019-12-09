from flask import Flask
from flaskext.mysql import MySQL, pymysql

app = Flask(__name__, static_url_path="")

app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "toor"
app.config["MYSQL_DATABASE_DB"] = "yugen_db"

mysql = MySQL(app, cursorClass = pymysql.cursors.DictCursor)

@app.route("/")
@app.route("/index")
def index_page():
    return app.send_static_file("index.html")











if __name__ == "__main__":
    app.run("0.0.0.0", 5000, threaded=True)