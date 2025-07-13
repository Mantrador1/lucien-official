# -*- coding: utf-8 -*-
import requests
import time

# ÃƒÅ½Ã‚Â¦ÃƒÂÃ…â€™ÃƒÂÃ‚ÂÃƒÂÃ¢â‚¬Å¾ÃƒÂÃ¢â‚¬Â°ÃƒÂÃ†â€™ÃƒÅ½Ã‚Â· ÃƒÂÃ‚ÂÃƒÂÃ¢â‚¬Â¦ÃƒÅ½Ã‚Â¸ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Â¯ÃƒÂÃ†â€™ÃƒÅ½Ã‚ÂµÃƒÂÃ¢â‚¬Â°ÃƒÅ½Ã‚Â½ ÃƒÅ½Ã‚Â±ÃƒÂÃ¢â€šÂ¬ÃƒÂÃ…â€™ lucien.cfg
config = {}
with open("lucien.cfg", "r") as f:
    for line in f:
        key, value = line.strip().split("=", 1)
        config[key.strip()] = value.strip()

TOKEN = config["TOKEN"]
CHAT_ID = os.getenv("CHAT_ID")
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
        print("ÃƒÂ¢Ã‚ÂÃ…â€™ ÃƒÅ½Ã‚Â£ÃƒÂÃ¢â‚¬Â ÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Â± get_updates:", e)
        return []

def send_message(chat_id, text):
    data = {"chat_id": chat_id, "text": text}
    try:
        requests.post(SEND_MESSAGE_URL, data=data)
    except Exception as e:
        print("ÃƒÂ¢Ã‚ÂÃ…â€™ ÃƒÅ½Ã‚Â£ÃƒÂÃ¢â‚¬Â ÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Â± send_message:", e)

# ÃƒÅ½Ã…Â¡ÃƒÂÃ‚ÂÃƒÂÃ‚ÂÃƒÅ½Ã‚Â¹ÃƒÅ½Ã‚Â¿ÃƒÂÃ¢â‚¬Å¡ ÃƒÅ½Ã‚Â²ÃƒÂÃ‚ÂÃƒÂÃ…â€™ÃƒÂÃ¢â‚¬Â¡ÃƒÅ½Ã‚Â¿ÃƒÂÃ¢â‚¬Å¡
while True:
    updates = get_updates()
    for update in updates:
        if "message" in update and "text" in update["message"]:
            user_input = update["message"]["text"]
            print("ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã‚Â© ÃƒÅ½Ã¢â‚¬ÂºÃƒÅ½Ã‚Â®ÃƒÂÃ¢â‚¬Â ÃƒÅ½Ã‚Â¸ÃƒÅ½Ã‚Â·ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚Âµ ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Â®ÃƒÅ½Ã‚Â½ÃƒÂÃ¢â‚¬Â¦ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Â±:", user_input)

            try:
                response = requests.post(API_URL, headers={"Authorization": f"Bearer {os.environ.get(\"OPENROUTER_API_KEY\", \"\")}"}, json={"prompt": user_input})
                reply = response.json().get("response", "ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â ÃƒÅ½Ã¢â‚¬ÂÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â½ ÃƒÂÃ¢â€šÂ¬ÃƒÅ½Ã‚Â®ÃƒÂÃ‚ÂÃƒÅ½Ã‚Âµ ÃƒÅ½Ã‚Â±ÃƒÂÃ¢â€šÂ¬ÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚Â½ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â·ÃƒÂÃ†â€™ÃƒÅ½Ã‚Â·.")
                send_message(CHAT_ID, reply)
            except Exception as e:
                print("ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â ÃƒÅ½Ã‚Â£ÃƒÂÃ¢â‚¬Â ÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Â± ÃƒÂÃ†â€™ÃƒÂÃ‚ÂÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚Â´ÃƒÅ½Ã‚ÂµÃƒÂÃ†â€™ÃƒÅ½Ã‚Â·ÃƒÂÃ¢â‚¬Å¡ ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Âµ Lucien API:", e)
    time.sleep(2)





