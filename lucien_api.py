# -*- coding: utf-8 -*-
from flask import Flask, request
import requests
import datetime
import json

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
AUTHORIZED_CHAT_ID = os.environ.get("CHAT_ID")
LOG_FILE = "logs/lucien_commands.log"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, headers={"Authorization": f"Bearer {os.environ.get(\"OPENROUTER_API_KEY\", \"\")}"}, json=payload)

def log_command(text):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {text}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("ÃƒÂ¢Ã…Â¾Ã‚Â¡ ÃƒÅ½Ã‚ÂÃƒÅ½Ã‚Â­ÃƒÅ½Ã‚Â¿ ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Â®ÃƒÅ½Ã‚Â½ÃƒÂÃ¢â‚¬Â¦ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Â± ÃƒÅ½Ã‚Â±ÃƒÂÃ¢â€šÂ¬ÃƒÂÃ…â€™ Telegram:")
    print(json.dumps(data, indent=4, ensure_ascii=False))

    if "message" in data and "chat" in data["message"]:
        chat_id = str(data["message"]["chat"]["id"])
        user_text = data["message"].get("text", "").lower()
        log_command(user_text)

        if chat_id != AUTHORIZED_CHAT_ID:
            send_message(chat_id, "ÃƒÂ°Ã…Â¸Ã…Â¡Ã‚Â« Unauthorized access.")
            return "unauthorized", 403

        if "status" in user_text:
            reply = "ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã‚Â¡ ÃƒÅ½Ã…Â¸ Lucien ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â¯ÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚Â±ÃƒÅ½Ã‚Â¹ ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚ÂµÃƒÂÃ‚ÂÃƒÅ½Ã‚Â³ÃƒÂÃ…â€™ÃƒÂÃ¢â‚¬Å¡ ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚Â±ÃƒÅ½Ã‚Â¹ ÃƒÅ½Ã‚Â±ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚Â¿ÃƒÂÃ‚ÂÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â¹."
        elif "ÃƒÅ½Ã‚Â­ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â³ÃƒÂÃ¢â‚¬Â¡ÃƒÅ½Ã‚Â¿" in user_text:
            reply = "ÃƒÂ°Ã…Â¸Ã‚Â§Ã‚Â  ÃƒÅ½Ã¢â‚¬Â¢ÃƒÅ½Ã‚ÂºÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â»ÃƒÂÃ…Â½ ÃƒÅ½Ã‚Â­ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â³ÃƒÂÃ¢â‚¬Â¡ÃƒÅ½Ã‚Â¿ ÃƒÂÃ¢â‚¬Â¦ÃƒÂÃ¢â€šÂ¬ÃƒÅ½Ã‚Â¿ÃƒÂÃ†â€™ÃƒÂÃ¢â‚¬Â¦ÃƒÂÃ†â€™ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â·ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Â¬ÃƒÂÃ¢â‚¬Å¾ÃƒÂÃ¢â‚¬Â°ÃƒÅ½Ã‚Â½..."
        elif "ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â¯ÃƒÂÃ†â€™ÃƒÅ½Ã‚Â±ÃƒÅ½Ã‚Â¹ ok" in user_text:
            reply = "ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ ÃƒÅ½Ã…Â¸ Lucien ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â¯ÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚Â±ÃƒÅ½Ã‚Â¹ ÃƒÂÃ…â€™ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Â± ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚Â±ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Â¬. ÃƒÅ½Ã‚Â£ÃƒÂÃ¢â‚¬Â¡ÃƒÅ½Ã‚Â¬ÃƒÂÃ‚ÂÃƒÅ½Ã‚Â±ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Âµ!"
        else:
            fname = data["message"]["from"].get("first_name", "ÃƒÅ½Ã‚Â¦ÃƒÅ½Ã‚Â¯ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Âµ")
            reply = f"ÃƒÂ°Ã…Â¸Ã¢â‚¬ËœÃ¢â‚¬Â¹ ÃƒÅ½Ã¢â‚¬Å“ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â¹ÃƒÅ½Ã‚Â± ÃƒÂÃ†â€™ÃƒÅ½Ã‚Â¿ÃƒÂÃ¢â‚¬Â¦ {fname}! ÃƒÅ½Ã¢â‚¬Â¢ÃƒÅ½Ã‚Â¯ÃƒÂÃ¢â€šÂ¬ÃƒÅ½Ã‚ÂµÃƒÂÃ¢â‚¬Å¡: ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ{user_text}ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â"

        send_message(chat_id, reply)

    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)





