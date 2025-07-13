# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

# ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ ÃƒÅ½Ã…â€œÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚Â®ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Â· ÃƒÅ½Ã‚Â±ÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚Â¬ IP (ÃƒÅ½Ã‚Â±ÃƒÂÃ¢â€šÂ¬ÃƒÅ½Ã‚Â»ÃƒÂÃ…â€™ dictionary ÃƒÂÃ¢â€šÂ¬ÃƒÂÃ‚ÂÃƒÅ½Ã‚Â¿ÃƒÂÃ†â€™ÃƒÂÃ¢â‚¬Â°ÃƒÂÃ‚ÂÃƒÅ½Ã‚Â¹ÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚Â¬)
memory = {}

# ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Â OpenRouter API Key
OPENROUTER_API_KEY = "sk-or-v1-ΔΩΣΕ_ΕΔΩ_ΤΟ_ΝΕΟ_ΚΛΕΙΔΙ"

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_input = data.get('prompt', '')
    user_ip = request.remote_addr

    if user_ip not in memory:
        memory[user_ip] = []

    memory[user_ip].append({"role": "user", "content": user_input})

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "dolphin-mixtral-8x7b",
        "messages": memory[user_ip],
        "max_tokens": 500
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)

    if response.status_code == 200:
        reply = response.json()['choices'][0]['message']['content']
        memory[user_ip].append({"role": "assistant", "content": reply})
        return jsonify({"response": reply})
    else:
        return jsonify({"response": "ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â ÃƒÅ½Ã‚Â£ÃƒÂÃ¢â‚¬Â ÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Â± ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Âµ OpenRouter API."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5050)





