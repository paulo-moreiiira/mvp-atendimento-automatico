
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def inicio():
    dispositivo = None

    if request.method == "POST":
        dispositivo = request.form.get("dispositivo", "")

    return render_template("index.html", dispositivo=dispositivo)


if __name__ == "__main__":
    app.run(debug=True)
