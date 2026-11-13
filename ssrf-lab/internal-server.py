from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>Internal Server</h1>
    <p>This server is only accessible from inside the network.</p>
    """


@app.route("/admin")
def admin():
    return """
    <h1>Internal Admin Panel</h1>
    <p style="color:red;">SECRET: Internal admin data</p>
    <p>Username: internal_admin</p>
    <p>Password: SuperSecret123</p>
    """


@app.route("/api/internal")
def internal_api():
    return {
        "service": "internal-api",
        "status": "running",
        "secret": "INTERNAL-SECRET-123"
    }


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5003)
