# -*- coding: utf-8 -*-
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "meta-llama/llama-3-70b-instruct")

@app.route("/")
def index():
    return "Lucien External Proxy is Running."

@app.route("/ask", methods=["POST"])
def ask_ai():
    data = request.json
    prompt = data.get("prompt", "")
    model = data.get("model", DEFAULT_MODEL)

    if not prompt:
        return jsonify({"error": "Prompt is required."}), 400

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(f"{OPENROUTER_BASE_URL}/chat/completions", headers=headers, json=payload)

    if response.status_code != 200:
        return jsonify({"error": "Failed to connect to OpenRouter.", "details": response.text}), 500

    result = response.json()
    answer = result.get("choices", [{}])[0].get("message", {}).get("content", "No response.")
    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(debug=True, port=5050)





