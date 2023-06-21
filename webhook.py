import os
import json
from flask import Flask, request

app = Flask(__name__)


@app.route("/webhook/inbound-message", methods=["POST"])
def inbound_message():
    try:
        data = request.get_json()

        # retrieve the list of artists
        artists = data["text"].split(",")

        with open("artists.json", "w") as f:
            json.dump({"artists": artists}, f)

        return "200"

    except Exception as e:
        pass


@app.route("/webhook/status", methods=["POST"])
def status():
    data = request.get_json()

    return "200"


if __name__ == "__main__":
    app.run(ssl_context="adhoc", host="0.0.0.0", port="8081", debug=True)
