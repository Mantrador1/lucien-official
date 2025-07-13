import requests

def call_shadow_mistral(prompt):
    try:
        res = requests.post("https://lucien-outside.fly.dev/ask", json={"prompt": prompt})
        return res.json().get("response", "?? No response from shadow model.")
    except Exception as e:
        return f"? Shadow model error: {str(e)}"





