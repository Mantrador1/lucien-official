import os
import time
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ASK_URL = "http://localhost:5000/ask"

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    if offset:
        url += f"?offset={offset}"
    try:
        return requests.get(url).json()
    except:
        return {}

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=data)
    except:
        pass

def forward_to_flask(message):
    try:
        response = requests.post(ASK_URL, json={"message": message})
        return response.text
    except:
        return "⚠️ Error contacting Flask."

def main():
    print("✅ Telegram polling ξεκίνησε")
    offset = None
    while True:
        updates = get_updates(offset)
        if "result" in updates:
            for update in updates["result"]:
                offset = update["update_id"] + 1
                if "message" in update and "text" in update["message"]:
                    text = update["message"]["text"]
                    if text.startswith("/ask "):
                        query = text[5:]
                        reply = forward_to_flask(query)
                        send_message(reply)
        time.sleep(2)

if __name__ == "__main__":
    main()
