# -*- coding: utf-8 -*-
import requests
import subprocess
import time

# === ÃƒÅ½Ã‚Â¡ÃƒÅ½Ã‚Â¥ÃƒÅ½Ã‹Å“ÃƒÅ½Ã…â€œÃƒÅ½Ã¢â€žÂ¢ÃƒÅ½Ã‚Â£ÃƒÅ½Ã¢â‚¬Â¢ÃƒÅ½Ã¢â€žÂ¢ÃƒÅ½Ã‚Â£ ===
TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = f"https://api.telegram.org/bot{TOKEN}/"
last_update_id = 0

def send_message(text):
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(URL + "sendMessage", data=data)

def get_updates():
    global last_update_id
    try:
        params = {"offset": last_update_id + 1, "timeout": 10}
        response = requests.get(URL + "getUpdates", params=params)
        result = response.json()["result"]
        return result
    except Exception as e:
        print("ÃƒÅ½Ã‚Â£ÃƒÂÃ¢â‚¬Â ÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Â± ÃƒÂÃ†â€™ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â¿ get_updates:", e)
        return []

def execute_command(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return e.output.decode("utf-8")
    except Exception as e:
        return f"ÃƒÅ½Ã‚Â£ÃƒÂÃ¢â‚¬Â ÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Â±: {str(e)}"

# === MAIN LOOP ===
print("ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂºÃ‚Â° Lucien Command Listener ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚ÂµÃƒÂÃ‚ÂÃƒÅ½Ã‚Â³ÃƒÂÃ…â€™ÃƒÂÃ¢â‚¬Å¡.")
send_message("ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂºÃ‚Â° Lucien Command Listener ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚ÂµÃƒÂÃ‚ÂÃƒÅ½Ã‚Â³ÃƒÂÃ…â€™ÃƒÂÃ¢â‚¬Å¡.")

while True:
    updates = get_updates()
    for update in updates:
        last_update_id = update["update_id"]
        message = update.get("message", {})
        text = message.get("text", "")
        sender_id = message.get("from", {}).get("id", 0)

        print(f"[{sender_id}] -> {text}")  # DEBUG

        if sender_id != CHAT_ID:
            send_message("ÃƒÂ¢Ã¢â‚¬ÂºÃ¢â‚¬Â ÃƒÅ½Ã¢â‚¬Â ÃƒÂÃ‚ÂÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚Â·ÃƒÂÃ†â€™ÃƒÅ½Ã‚Â· ÃƒÂÃ¢â€šÂ¬ÃƒÂÃ‚ÂÃƒÂÃ…â€™ÃƒÂÃ†â€™ÃƒÅ½Ã‚Â²ÃƒÅ½Ã‚Â±ÃƒÂÃ†â€™ÃƒÅ½Ã‚Â·ÃƒÂÃ¢â‚¬Å¡.")
            continue

        if not text:
            continue

        result = execute_command(text)
        if not result.strip():
            result = "ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ ÃƒÅ½Ã¢â‚¬Â¢ÃƒÅ½Ã‚Â½ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â¿ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Â® ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚ÂºÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Â­ÃƒÂÃ†â€™ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â·ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚Âµ ÃƒÂÃ¢â‚¬Â¡ÃƒÂÃ¢â‚¬Â°ÃƒÂÃ‚ÂÃƒÅ½Ã‚Â¯ÃƒÂÃ¢â‚¬Å¡ ÃƒÅ½Ã‚Â­ÃƒÅ½Ã‚Â¾ÃƒÅ½Ã‚Â¿ÃƒÅ½Ã‚Â´ÃƒÅ½Ã‚Â¿."
        elif len(result) > 4000:
            result = result[:4000] + "\n...ÃƒÅ½Ã‚Â±ÃƒÂÃ¢â€šÂ¬ÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚Â½ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â·ÃƒÂÃ†â€™ÃƒÅ½Ã‚Â· ÃƒÂÃ¢â€šÂ¬ÃƒÅ½Ã‚ÂµÃƒÂÃ‚ÂÃƒÅ½Ã‚Â¹ÃƒÅ½Ã‚ÂºÃƒÂÃ…â€™ÃƒÂÃ¢â€šÂ¬ÃƒÅ½Ã‚Â·ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚Âµ."

        send_message(f"ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã‚Â¤ ÃƒÅ½Ã¢â‚¬ËœÃƒÂÃ¢â€šÂ¬ÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚Â½ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â·ÃƒÂÃ†â€™ÃƒÅ½Ã‚Â·:\n{result}")
    time.sleep(2)





