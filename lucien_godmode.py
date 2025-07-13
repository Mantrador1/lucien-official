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
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        res.raise_for_status()
        raw = res.json()
        print("\n📥 RAW JSON RESPONSE:\n", json.dumps(raw, indent=2, ensure_ascii=False))

        # 🔍 Εξαγωγή απάντησης από όπου υπάρχει
        reply = (
            raw.get("choices", [{}])[0]
               .get("message", {})
               .get("content")
            or raw.get("output")
            or raw.get("message")
            or "⚠️ No valid response format found."
        )

        return jsonify({"response": reply})

    except Exception as e:
        try:
            print("\n❗ RAW TEXT ERROR:\n", res.text)
        except:
            print("❗ No response text to show.")
        return jsonify({"response": f"⚠️ Σφάλμα AI: {e}"})

app.run(host="0.0.0.0", port=8080)





