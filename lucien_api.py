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
    requests.post(url, json=payload)

def log_command(text):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {text}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("âž¡ ÎÎ­Î¿ Î¼Î®Î½Ï…Î¼Î± Î±Ï€ÏŒ Telegram:")
    print(json.dumps(data, indent=4, ensure_ascii=False))

    if "message" in data and "chat" in data["message"]:
        chat_id = str(data["message"]["chat"]["id"])
        user_text = data["message"].get("text", "").lower()
        log_command(user_text)

        if chat_id != AUTHORIZED_CHAT_ID:
            send_message(chat_id, "ðŸš« Unauthorized access.")
            return "unauthorized", 403

        if "status" in user_text:
            reply = "ðŸ“¡ ÎŸ Lucien ÎµÎ¯Î½Î±Î¹ ÎµÎ½ÎµÏÎ³ÏŒÏ‚ ÎºÎ±Î¹ Î±ÎºÎ¿ÏÎµÎ¹."
        elif "Î­Î»ÎµÎ³Ï‡Î¿" in user_text:
            reply = "ðŸ§  Î•ÎºÏ„ÎµÎ»ÏŽ Î­Î»ÎµÎ³Ï‡Î¿ Ï…Ï€Î¿ÏƒÏ…ÏƒÏ„Î·Î¼Î¬Ï„Ï‰Î½..."
        elif "ÎµÎ¯ÏƒÎ±Î¹ ok" in user_text:
            reply = "âœ… ÎŸ Lucien ÎµÎ¯Î½Î±Î¹ ÏŒÎ»Î± ÎºÎ±Î»Î¬. Î£Ï‡Î¬ÏÎ±Î¼Îµ!"
        else:
            fname = data["message"]["from"].get("first_name", "Î¦Î¯Î»Îµ")
            reply = f"ðŸ‘‹ Î“ÎµÎ¹Î± ÏƒÎ¿Ï… {fname}! Î•Î¯Ï€ÎµÏ‚: â€œ{user_text}â€"

        send_message(chat_id, reply)

    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)