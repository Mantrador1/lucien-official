# -*- coding: utf-8 -*-
import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
RAILWAY_API_URL = os.environ.get("RAILWAY_API_URL") or "http://localhost:5050/ask"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, headers={"Authorization": f"Bearer {os.environ.get(\"OPENROUTER_API_KEY\", \"\")}"}, json={"chat_id": chat_id, "text": text})

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if "message" in data and "text" in data["message"]:
        user_msg = data["message"]["text"]
        chat_id = data["message"]["chat"]["id"]

        try:
            res = requests.post(RAILWAY_API_URL, headers={"Authorization": f"Bearer {os.environ.get(\"OPENROUTER_API_KEY\", \"\")}"}, json={"prompt": user_msg})
            ai_response = res.json().get("response", "?? Error from AI")
        except Exception as e:
            ai_response = f"?? Exception: {e}"

        send_message(chat_id, ai_response)

    return "ok"
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))





