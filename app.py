import os
import subprocess
from flask import Flask, render_template, request, session, redirect
from flask_wtf.csrf import CSRFProtect, CSRFError, validate_csrf
import requests

app = Flask(__name__)

app.config["SECRET_KEY"] = "my-secret-key"


users = {
    "viner": {
        "password": "viner123",
        "email": "viner@example.com"
    },
    "carlos": {
        "password": "carlos123",
        "email": "carlos@example.com"
    }
}

csrf = CSRFProtect(app)

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template(
        "csrf_error.html",
        reason=e.description
    ), 400

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

vulnerable_messages = []
secure_messages = []

@app.route("/")
def home():
    return render_template("index.html")


# Reflected XSS
@app.route("/xss")
def xss():
    name = request.args.get("name")
    return render_template("xss.html", name=name)


@app.route("/xss-secure")
def xss_secure():
    name = request.args.get("name")
    return render_template("xss_secure.html", name=name)


# About
@app.route("/about")
def about():
    return render_template("about.html")


# Stored XSS
@app.route("/stored-xss", methods=["GET", "POST"])
def stored_xss():
    if request.method == "POST":
        message = request.form.get("message")

        if message:
            vulnerable_messages.append(message)

    return render_template(
        "xss_stored.html",
        messages=vulnerable_messages
    )


@app.route("/stored-xss-secure", methods=["GET", "POST"])
def stored_xss_secure():
    if request.method == "POST":
        message = request.form.get("message")

        if message:
            secure_messages.append(message)

    return render_template(
        "xss_stored_secure.html",
        messages=secure_messages
    )


# DOM XSS
@app.route("/dom-xss")
def dom_xss():
    return render_template("xss_dom.html")


@app.route("/dom-xss-secure")
def dom_xss_secure():
    return render_template("xss_dom_secure.html")


# File Upload - Vulnerable
@app.route("/upload", methods=["GET", "POST"])
def upload():
    uploaded = None

    if request.method == "POST":
        file = request.files.get("file")

        if file and file.filename:
            filename = file.filename

            file.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

            uploaded = filename

    return render_template(
        "upload.html",
        uploaded=uploaded
    )


# File Upload - Secure
@app.route("/upload-secure", methods=["GET", "POST"])
def upload_secure():
    uploaded = None
    error = None

    if request.method == "POST":
        file = request.files.get("file")

        if not file or not file.filename:
            error = "Please select a file."

        else:
            filename = file.filename

            allowed = ["txt", "jpg", "png"]

            if "." not in filename:
                error = "File must have an extension."

            else:
                extension = filename.rsplit(".", 1)[1].lower()

                if extension in allowed:
                    file.save(
                        os.path.join(
                            app.config["UPLOAD_FOLDER"],
                            filename
                        )
                    )

                    uploaded = filename

                else:
                    error = "This file type is not allowed."

    return render_template(
        "upload_secure.html",
        uploaded=uploaded,
        error=error
    )

# Path Traversal
@app.route("/traversal")
def traversal():
    filename = request.args.get("filename")
    content = None

    if filename:
        path = os.path.join("files", filename)

        try:
            with open(path, "r") as file:
                content = file.read()
        except Exception:
            content = "File not found."

    return render_template(
        "traversal.html",
        content=content
    )

# Path Traversal - Secure
@app.route("/traversal-secure")
def traversal_secure():
    filename = request.args.get("filename")
    content = None
    error = None

    if filename:
        safe_name = os.path.basename(filename)

        if safe_name != filename:
            error = "Invalid filename."
        else:
            path = os.path.join("files", safe_name)

            if os.path.isfile(path):
                with open(path, "r") as file:
                    content = file.read()
            else:
                error = "File not found."

    return render_template(
        "traversal_secure.html",
        content=content,
        error=error
    )

# Command Injection
@app.route("/command")
def command():
    host = request.args.get("host")
    output = None

    if host:
        command = "ping -c 2 " + host
        output = os.popen(command).read()

    return render_template(
        "command.html",
        output=output
    )

# Command Injection - Secure
@app.route("/command-secure")
def command_secure():
    host = request.args.get("host")
    output = None
    error = None

    if host:
        try:
            result = subprocess.run(
                ["ping", "-c", "2", host],
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout

        except Exception:
            error = "Invalid host."

    return render_template(
        "command_secure.html",
        output=output,
        error=error
    )

#csrf-login
@app.route("/csrf-login", methods=["GET", "POST"])
def csrf_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        print("USERNAME:", repr(username))
        print("PASSWORD:", repr(password))

        if username not in users:
            return render_template(
                "csrf_login.html",
                error="Invalid username or password"
            )

        if users[username]["password"] != password:
            return render_template(
                "csrf_login.html",
                error="Invalid username or password"
            )

        session["csrf_user"] = username

        return redirect("/csrf-account")

    return render_template(
        "csrf_login.html",
        error=""
    )


#csrf-logout
@app.route("/csrf-logout")
def csrf_logout():
    session.pop("csrf_user", None)
    return redirect("/csrf-login")

#csrf-account
@app.route("/csrf-account")
def csrf_account():
    username = session.get("csrf_user")

    if not username:
        return redirect("/csrf-login")

    return render_template(
        "csrf_account.html",
        username=username,
        email=users[username]["email"]
    )


# CSRF-Vulnerable
@app.route("/change-email-vulnerable", methods=["POST"])
@csrf.exempt
def change_email_vulnerable():
    username = session.get("csrf_user")

    if not username:
        return "Please login first", 401

    new_email = request.form.get("email")

    users[username]["email"] = new_email

    return render_template(
        "csrf_result.html",
        username=username,
        email=new_email,
        vulnerable=True
    )


#ATTACKER
@app.route("/csrf-attacker")
def csrf_attacker():
    return render_template(
        "csrf_attacker.html",
        username="carlos",
        current_user="carlos"
    )

# CSRF-Secure
@app.route("/csrf-secure")
def csrf_secure():
    username = session.get("csrf_user")

    if not username:
        return redirect("/csrf-login")

    return render_template(
        "csrf_secure.html",
        username=username,
        email=users[username]["email"]
    )


@app.route("/csrf-secure-change-email", methods=["POST"])
def csrf_secure_change_email():
    username = session.get("csrf_user")

    if not username:
        return "Please login first", 401


    try:
        validate_csrf(request.form.get("csrf_token"))
    except Exception:
        return "CSRF token is missing or invalid", 400

    new_email = request.form.get("email")

    if not new_email:
        return "Email is required", 400


    users[username]["email"] = new_email

    return render_template(
        "csrf_secure_result.html",
        username=username,
        email=new_email
    )


# SSRF - Vulnerable

@app.route("/ssrf", methods=["GET", "POST"])
@csrf.exempt
def ssrf():
    result = None
    error = None

    if request.method == "POST":
        url = request.form.get("url")

        if not url:
            error = "URL is required"
        else:
            try:
                response = requests.get(url, timeout=5)

                result = {
                    "status": response.status_code,
                    "content": response.text
                }

            except requests.RequestException as e:
                error = str(e)

    return render_template(
        "ssrf.html",
        result=result,
        error=error
    )


# SSRF - Secure

@app.route("/ssrf-secure", methods=["GET", "POST"])
def ssrf_secure():
    result = None
    error = None

    if request.method == "POST":
        url = request.form.get("url")

        if not url:
            error = "URL is required"
        elif not url.startswith("https://example.com"):
            error = "URL is not allowed"
        else:
            try:
                response = requests.get(url, timeout=5)

                result = {
                    "status": response.status_code,
                    "content": response.text
                }

            except requests.RequestException as e:
                error = str(e)

    return render_template(
        "ssrf_secure.html",
        result=result,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)

