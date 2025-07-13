from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "Lucien is alive!", 200

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    model = data.get("model")
    prompt = data.get("prompt")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "prompt": prompt
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": response.text}), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)




