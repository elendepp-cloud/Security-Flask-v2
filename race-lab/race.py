from flask import Flask, render_template
import time
import threading

app = Flask(__name__)

balance = 100
coupon_used = False
lock = threading.Lock()


@app.route("/")
def home():
    return render_template(
        "race.html",
        balance=balance,
        coupon_used=coupon_used
    )


@app.route("/vulnerable")
def vulnerable():

    global balance, coupon_used

    if coupon_used:
        return "Coupon already used!"

    time.sleep(2)

    balance -= 10
    coupon_used = True

    return f"Coupon applied! Balance: ${balance}"


@app.route("/secure")
def secure():

    global balance, coupon_used

    with lock:

        if coupon_used:
            return "Coupon already used!"

        time.sleep(2)

        balance -= 10
        coupon_used = True

        return f"Coupon applied! Balance: ${balance}"


if __name__ == "__main__":
    app.run(port=5005, threaded=True)
