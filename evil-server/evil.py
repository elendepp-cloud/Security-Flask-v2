from flask import Flask, render_template

app = Flask(__name__)


@app.route("/ad")
def ad():
    return render_template("ad.html")


if __name__ == "__main__":
    app.run(port=5001, debug=True)
