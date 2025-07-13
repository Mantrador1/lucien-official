# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
REMOTE_LUCIEN_URL = "https://lucien-maverick-node.up.railway.app/ask"

@app.route("/relay", methods=["POST"])
def relay():
    data = request.get_json()
    try:
        response = requests.post(REMOTE_LUCIEN_URL, json=data)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({ "error": str(e) }), 500

if __name__ == "__main__":
    app.run(port=5050)





