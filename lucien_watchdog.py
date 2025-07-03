import requests
import time
import logging

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
CHECK_INTERVAL = 60  # Î­Î»ÎµÎ³Ï‡Î¿Ï‚ ÎºÎ¬Î¸Îµ 60 Î´ÎµÏ…Ï„ÎµÏÏŒÎ»ÎµÏ€Ï„Î±

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
            logging.warning("[TOKEN EXPIRED] ðŸ”¥ Î¤Î¿ Telegram Bot Token Ï†Î±Î¯Î½ÎµÏ„Î±Î¹ invalid!")
            send_alert("âš ï¸ Î¤Î¿ Telegram Bot Token Î­Ï€Î±ÏˆÎµ Î½Î± Î¹ÏƒÏ‡ÏÎµÎ¹! Î§ÏÎµÎ¹Î¬Î¶ÎµÏ„Î±Î¹ Î½Î­Î¿.")
        else:
            logging.info("[TOKEN VALID] âœ… Î¤Î¿ token ÎµÎ¯Î½Î±Î¹ Î­Î³ÎºÏ…ÏÎ¿.")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()