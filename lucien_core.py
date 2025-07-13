# -*- coding: utf-8 -*-
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

    print(f"ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã‚Â¥ Incoming message from {chat_id}: {text}")

    if text.startswith("/"):
        response = route_command(chat_id, text)
    else:
        response = f"ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¢ ÃƒÅ½Ã‹â€ ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Â±ÃƒÅ½Ã‚Â²ÃƒÅ½Ã‚Â± ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â¿ ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Â®ÃƒÅ½Ã‚Â½ÃƒÂÃ¢â‚¬Â¦ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Â¬ ÃƒÂÃ†â€™ÃƒÅ½Ã‚Â¿ÃƒÂÃ¢â‚¬Â¦: \"{text}\""

    # ÃƒÅ½Ã¢â‚¬Â¢ÃƒÅ½Ã‚Â´ÃƒÂÃ…Â½ ÃƒÅ½Ã‚Â¼ÃƒÂÃ¢â€šÂ¬ÃƒÅ½Ã‚Â¿ÃƒÂÃ‚ÂÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â¯ÃƒÂÃ¢â‚¬Å¡ ÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚Â± ÃƒÂÃ†â€™ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â¯ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â¹ÃƒÂÃ¢â‚¬Å¡ ÃƒÅ½Ã‚Â±ÃƒÂÃ¢â€šÂ¬ÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚Â½ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â·ÃƒÂÃ†â€™ÃƒÅ½Ã‚Â· ÃƒÂÃ†â€™ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â¿ Telegram ÃƒÅ½Ã‚Â±ÃƒÅ½Ã‚Â½ ÃƒÅ½Ã‚Â¸ÃƒÅ½Ã‚Â­ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â¹ÃƒÂÃ¢â‚¬Å¡
    print(f"ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã‚Â¤ Response: {response}")
    return {"ok": True}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)





