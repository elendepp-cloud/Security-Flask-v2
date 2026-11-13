
from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

DATABASE = "users.db"


def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT,
            password TEXT
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM users")

    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO users VALUES ('admin', 'admin123')"
        )

    conn.commit()
    conn.close()


@app.route("/login-vulnerable", methods=["GET", "POST"])
def login_vulnerable():
    message = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        query = f"""
            SELECT * FROM users
            WHERE username = '{username}'
            AND password = '{password}'
        """

        print("DEBUG SQL:", repr(query))

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()

        if user:
            message = "Login successful!"
        else:
            message = "Login failed!"

    return render_template("login.html", message=message)


@app.route("/login-secure", methods=["GET", "POST"])
def login_secure():
    message = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        query = """
            SELECT * FROM users
            WHERE username = ?
            AND password = ?
        """

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            message = "Login successful!"
        else:
            message = "Login failed!"

    return render_template("login_secure.html", message=message)


if __name__ == "__main__":
    create_database()
    app.run(port=5004, debug=True)
