# -*- coding: utf-8 -*-
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "orca-mini:latest"

def ask_lucien(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        res = requests.post(OLLAMA_URL, json=payload)
        res.raise_for_status()
        result = res.json()
        print("\n📥 RAW RESPONSE:\n", result)
        return result.get("response", "❌ No response.")
    except Exception as e:
        return f"❌ Error: {e}"

if __name__ == "__main__":
    while True:
        user_input = input("\n🧠 Ερώτηση προς Lucien: ")
        if user_input.lower() in ["exit", "quit", "ξέξιτ"]:
            break
        answer = ask_lucien(user_input)
        print(f"\n🤖 Lucien:\n{answer}")





