from flask import Flask, request, render_template, redirect, url_for
import jwt
import datetime

app = Flask(__name__)

SECRET_KEY = "my-secret-key"

# Demo users for this local lab
users = {
    "admin": {
        "password": "admin123",
        "role": "admin"
    },
    "carlos": {
        "password": "carlos123",
        "role": "user"
    }
}


@app.route("/")
def register():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def do_register():
    username = request.form["username"]
    password = request.form["password"]

    if username in users:
        return "Username already exists!"

    users[username] = {
        "password": password,
        "role": "user"
    }

    return redirect(url_for("login"))


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def do_login():
    username = request.form["username"]
    password = request.form["password"]

    user = users.get(username)

    if not user or user["password"] != password:
        return "Invalid username or password", 401

    token = jwt.encode(
        {
            "username": username,
            "role": user["role"],
            "exp": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(minutes=30)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return render_template("token.html", token=token)


@app.route("/vulnerable")
def vulnerable():
    token = request.args.get("token", "")

    try:
        # Intentionally vulnerable: does not verify JWT signature
        data = jwt.decode(
            token,
            options={
                "verify_signature": False,
                "verify_exp": False
            }
        )

        return render_template(
            "vulnerable.html",
            username=data.get("username"),
            role=data.get("role")
        )

    except jwt.InvalidTokenError as error:
        return f"Invalid token: {error}", 400


@app.route("/secure")
def secure():
    token = request.args.get("token", "")

    try:
        # Secure version: verifies the JWT signature
        data = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return render_template(
            "secure.html",
            username=data.get("username"),
            role=data.get("role")
        )

    except jwt.InvalidTokenError:
        return "Invalid token", 401


if __name__ == "__main__":
    app.run(port=5006, debug=True)
