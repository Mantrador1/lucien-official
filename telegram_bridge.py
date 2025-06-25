import requests
import time

# Φόρτωση ρυθμίσεων από lucien.cfg
config = {}
with open("lucien.cfg", "r") as f:
    for line in f:
        key, value = line.strip().split("=", 1)
        config[key.strip()] = value.strip()

TOKEN = config["TOKEN"]
CHAT_ID = config["CHAT_ID"]
API_URL = config["API_URL"]

GET_UPDATES_URL = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
SEND_MESSAGE_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

last_update_id = None

def get_updates():
    global last_update_id
    params = {"timeout": 10, "offset": last_update_id}
    try:
        response = requests.get(GET_UPDATES_URL, params=params)
        result = response.json().get("result", [])
        if result:
            last_update_id = result[-1]["update_id"] + 1
        return result
    except Exception as e:
        print("❌ Σφάλμα get_updates:", e)
        return []

def send_message(chat_id, text):
    data = {"chat_id": chat_id, "text": text}
    try:
        requests.post(SEND_MESSAGE_URL, data=data)
    except Exception as e:
        print("❌ Σφάλμα send_message:", e)

# Κύριος βρόχος
while True:
    updates = get_updates()
    for update in updates:
        if "message" in update and "text" in update["message"]:
            user_input = update["message"]["text"]
            print("📩 Λήφθηκε μήνυμα:", user_input)

            try:
                response = requests.post(API_URL, json={"prompt": user_input})
                reply = response.json().get("response", "⚠️ Δεν πήρε απάντηση.")
                send_message(CHAT_ID, reply)
            except Exception as e:
                print("⚠️ Σφάλμα σύνδεσης με Lucien API:", e)
    time.sleep(2)
