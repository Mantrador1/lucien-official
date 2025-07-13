import requests
import time

BOT_TOKEN = "7121107982:AAHEs4EGv57F2J3kI8AxFeTKHFY5hgq8yX8"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
OFFSET = 0

def send_message(chat_id, text):
    try:
        requests.post(f"{BASE_URL}/sendMessage", json={"chat_id": chat_id, "text": text})
    except:
        pass

def handle_update(update):
    try:
        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "")

        if not chat_id or not text:
            return

        print(f"📩 Από {chat_id}: {text}")

        # Send to Claude via Flask
        response = requests.post("http://localhost:5000/ask", json={"message": {"text": text}})
        result = response.json()

        if "reply" in result:
            send_message(chat_id, result["reply"])
        else:
            send_message(chat_id, "⚠️ Ο Claude δεν απάντησε σωστά.")
    except Exception as e:
        send_message(chat_id, f"❌ Σφάλμα: {str(e)}")

def main():
    global OFFSET
    print("🤖 Telegram polling ξεκίνησε.")
    while True:
        try:
            response = requests.get(f"{BASE_URL}/getUpdates", params={"offset": OFFSET + 1, "timeout": 30})
            updates = response.json().get("result", [])
            for update in updates:
                OFFSET = update["update_id"]
                handle_update(update)
        except Exception as e:
            print(f"⛔ Polling error: {e}")
        time.sleep(1)

if __name__ == "__main__":
    main()
