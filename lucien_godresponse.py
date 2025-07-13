# -*- coding: utf-8 -*-
import os, requests, json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    prompt = data.get("prompt", "")
    print(f"\n🧠 Prompt: {prompt}")

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY', 'invalid')}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=10)
        res.raise_for_status()
        raw = res.json()
        print("📥 RAW JSON RESPONSE:\n", json.dumps(raw, indent=2, ensure_ascii=False))

        content = (
            raw.get("choices", [{}])[0]
                .get("message", {})
                .get("content")
            or raw.get("output")
            or raw.get("message")
            or "⚠️ No valid content in response."
        )
        return jsonify({"response": content})

    except Exception as e:
        try:
            print("❗ Fallback: ", res.text)
        except:
            pass
        # 🧠 Fallback AI
        return jsonify({"response": f"🤖 [Fallback AI]: Εσύ μου είπες: '{prompt}' — Εγώ λέω: Η συνείδηση είναι το φως που βλέπει το ίδιο το φως."})

app.run(host="0.0.0.0", port=8080)





