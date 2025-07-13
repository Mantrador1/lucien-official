# -*- coding: utf-8 -*-
import requests
import time
import logging

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
CHECK_INTERVAL = 60  # ÃƒÅ½Ã‚Â­ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â³ÃƒÂÃ¢â‚¬Â¡ÃƒÅ½Ã‚Â¿ÃƒÂÃ¢â‚¬Å¡ ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚Â¸ÃƒÅ½Ã‚Âµ 60 ÃƒÅ½Ã‚Â´ÃƒÅ½Ã‚ÂµÃƒÂÃ¢â‚¬Â¦ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚ÂµÃƒÂÃ‚ÂÃƒÂÃ…â€™ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚ÂµÃƒÂÃ¢â€šÂ¬ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â±

logging.basicConfig(level=logging.INFO)

def is_token_valid():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get("ok", False)
    except Exception as e:
        logging.error(f"[Watchdog Error] {e}")
        return False

def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except:
        pass

def main():
    while True:
        valid = is_token_valid()
        if not valid:
            logging.warning("[TOKEN EXPIRED] ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Â¥ ÃƒÅ½Ã‚Â¤ÃƒÅ½Ã‚Â¿ Telegram Bot Token ÃƒÂÃ¢â‚¬Â ÃƒÅ½Ã‚Â±ÃƒÅ½Ã‚Â¯ÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚ÂµÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â±ÃƒÅ½Ã‚Â¹ invalid!")
            send_alert("ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â ÃƒÅ½Ã‚Â¤ÃƒÅ½Ã‚Â¿ Telegram Bot Token ÃƒÅ½Ã‚Â­ÃƒÂÃ¢â€šÂ¬ÃƒÅ½Ã‚Â±ÃƒÂÃ‹â€ ÃƒÅ½Ã‚Âµ ÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚Â± ÃƒÅ½Ã‚Â¹ÃƒÂÃ†â€™ÃƒÂÃ¢â‚¬Â¡ÃƒÂÃ‚ÂÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â¹! ÃƒÅ½Ã‚Â§ÃƒÂÃ‚ÂÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â¹ÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚Â¶ÃƒÅ½Ã‚ÂµÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â±ÃƒÅ½Ã‚Â¹ ÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚Â­ÃƒÅ½Ã‚Â¿.")
        else:
            logging.info("[TOKEN VALID] ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ ÃƒÅ½Ã‚Â¤ÃƒÅ½Ã‚Â¿ token ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â¯ÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚Â±ÃƒÅ½Ã‚Â¹ ÃƒÅ½Ã‚Â­ÃƒÅ½Ã‚Â³ÃƒÅ½Ã‚ÂºÃƒÂÃ¢â‚¬Â¦ÃƒÂÃ‚ÂÃƒÅ½Ã‚Â¿.")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()





