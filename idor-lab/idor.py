from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.config["SECRET_KEY"] = "idor-secret-key"

users = {
    "wiener": {
        "password": "wiener123"
    },
    "carlos": {
        "password": "carlos123"
    }
}

orders = {
    1001: {
        "owner": "wiener",
        "product": "Laptop",
        "price": "$1200",
        "status": "Shipped"
    },
    1002: {
        "owner": "carlos",
        "product": "Gaming Keyboard",
        "price": "$150",
        "status": "Processing"
    }
}


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username]["password"] == password:
            session["user"] = username
            return redirect("/account")

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html", error="")


@app.route("/account")
def account():
    username = session.get("user")

    if not username:
        return redirect("/login")

    return render_template(
        "account.html",
        username=username
    )


@app.route("/idor-order/<int:order_id>")
def idor_order(order_id):
    username = session.get("user")

    if not username:
        return redirect("/login")

    order = orders.get(order_id)

    if not order:
        return "Order not found", 404

    # INTENTIONALLY VULNERABLE
    # There is no check that the order belongs to the logged-in user.

    return render_template(
        "order.html",
        username=username,
        order_id=order_id,
        order=order
    )


if __name__ == "__main__":
    app.run(port=5002, debug=True)
