# -*- coding: utf-8 -*-
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(force=True)
    if not data or "prompt" not in data:
        return jsonify({"error": "Missing 'prompt' in request"}), 400

    prompt = data["prompt"]
    url = "https://openrouter.ai/api/v1/chat/completions"
    payload = {
        "model": "dolphin-mixtral-8x7b",
        "messages": [{"role": "user", "content": prompt}]
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, headers={"Authorization": f"Bearer {os.environ.get(\"OPENROUTER_API_KEY\", \"\")}"}, json=payload, headers=headers)
        response.raise_for_status()
        return jsonify(response.json()), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)





