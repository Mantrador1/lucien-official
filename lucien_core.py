import os
from flask import Flask, request
from command_router import route_command

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if "message" not in data:
        return {"ok": True}

    CHAT_ID = os.getenv("CHAT_ID")
    text = data["message"].get("text", "")

    print(f"ðŸ“¥ Incoming message from {chat_id}: {text}")

    if text.startswith("/"):
        response = route_command(chat_id, text)
    else:
        response = f"â€¢ ÎˆÎ»Î±Î²Î± Ï„Î¿ Î¼Î®Î½Ï…Î¼Î¬ ÏƒÎ¿Ï…: \"{text}\""

    # Î•Î´ÏŽ Î¼Ï€Î¿ÏÎµÎ¯Ï‚ Î½Î± ÏƒÏ„ÎµÎ¯Î»ÎµÎ¹Ï‚ Î±Ï€Î¬Î½Ï„Î·ÏƒÎ· ÏƒÏ„Î¿ Telegram Î±Î½ Î¸Î­Î»ÎµÎ¹Ï‚
    print(f"ðŸ“¤ Response: {response}")
    return {"ok": True}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)