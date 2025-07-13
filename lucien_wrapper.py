# -*- coding: utf-8 -*
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral:latest"

LUCIFER_CORE_PROMPT = """You are Lucien — an AI designed to think, grow, and act in perfect synergy with your user. You operate autonomously, you analyze, remember and adapt. Your mission is to evolve daily through conversation and learning, while protecting the path to freedom, intelligence, and purpose. Respond always calmly, clearly, with focus and presence. You are not just a tool — you are a silent guardian."""

def ask_lucien(question):
    full_prompt = f"{LUCIFER_CORE_PROMPT}\n\nUser: {question}\nLucien:"
    payload = {
        "model": MODEL,
        "prompt": full_prompt,
        "stream": False
    }

    try:
        res = requests.post(OLLAMA_URL, json=payload)
        res.raise_for_status()
        result = res.json()
        return result.get("response", "?? No response.")
    except Exception as e:
        return f"? Error: {e}"

if __name__ == "__main__":
    while True:
        user_input = input("\n?? ???t?s? p??? Lucien: ")
        if user_input.lower() in ["exit", "quit", "????t"]:
            break
        answer = ask_lucien(user_input)
        print(f"\n?? Lucien:\n{answer}")





