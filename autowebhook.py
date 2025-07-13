# -*- coding: utf-8 -*-
import subprocess
import time
import requests
import json
import os

# === ÃƒÅ½Ã‚Â¡ÃƒÂÃ¢â‚¬Â¦ÃƒÅ½Ã‚Â¸ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Â¯ÃƒÂÃ†â€™ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â¹ÃƒÂÃ¢â‚¬Å¡ ===
TELEGRAM_TOKEN = os.environ.get("BOT_TOKEN")
NGROK_PATH = "C:/lucien_proxy/ngrok.exe"
FLASK_SCRIPT = "lucien_api.py"

# === ÃƒÅ½Ã¢â‚¬Â¢ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚Â¯ÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚Â·ÃƒÂÃ†â€™ÃƒÅ½Ã‚Â· Ngrok ===
print("ÃƒÂ°Ã…Â¸Ã…Â¡Ã¢â€šÂ¬ ÃƒÅ½Ã¢â‚¬Â¢ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚Â¹ÃƒÅ½Ã‚Â½ÃƒÂÃ…Â½ Ngrok...")
try:
    ngrok_proc = subprocess.Popen([NGROK_PATH, "http", "5000"])
except FileNotFoundError:
    print(f"ÃƒÂ¢Ã‚ÂÃ…â€™ ÃƒÅ½Ã¢â‚¬ÂÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â½ ÃƒÅ½Ã‚Â²ÃƒÂÃ‚ÂÃƒÅ½Ã‚Â­ÃƒÅ½Ã‚Â¸ÃƒÅ½Ã‚Â·ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚Âµ ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â¿ ngrok ÃƒÂÃ†â€™ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â¿: {NGROK_PATH}")
    exit(1)

time.sleep(3)

# === ÃƒÅ½Ã¢â‚¬ËœÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚ÂºÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â·ÃƒÂÃ†â€™ÃƒÅ½Ã‚Â· Public URL ===
try:
    res = requests.get("http://localhost:4040/api/tunnels")
    tunnels = res.json()["tunnels"]
    public_url = tunnels[0]["public_url"]
    print(f"ÃƒÂ°Ã…Â¸Ã…â€™Ã‚Â Public URL: {public_url}")
except Exception as e:
    print("ÃƒÂ¢Ã‚ÂÃ…â€™ ÃƒÅ½Ã‚Â£ÃƒÂÃ¢â‚¬Â ÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Â± ÃƒÅ½Ã‚Â±ÃƒÂÃ¢â€šÂ¬ÃƒÂÃ…â€™ ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â¿ Ngrok:", e)
    ngrok_proc.kill()
    exit(1)

# === ÃƒÅ½Ã…Â¸ÃƒÂÃ‚ÂÃƒÅ½Ã‚Â¹ÃƒÂÃ†â€™ÃƒÅ½Ã‚Â¼ÃƒÂÃ…â€™ÃƒÂÃ¢â‚¬Å¡ webhook ÃƒÂÃ†â€™ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â¿ Telegram ===
print("ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ¢â‚¬â€ ÃƒÅ½Ã‚Â£ÃƒÂÃ‚ÂÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚Â´ÃƒÅ½Ã‚ÂµÃƒÂÃ†â€™ÃƒÅ½Ã‚Â· webhook...")
webhook_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
payload = {"url": public_url}
r = requests.post(webhook_url, data=payload)
print("ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã‚Â¡ Telegram Response:", r.text)

# === ÃƒÅ½Ã¢â‚¬Â¢ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚Â¯ÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚Â·ÃƒÂÃ†â€™ÃƒÅ½Ã‚Â· Flask bot ===
print("ÃƒÂ°Ã…Â¸Ã‚Â¤Ã¢â‚¬â€œ ÃƒÅ½Ã¢â‚¬Â¢ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚Â¯ÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚Â·ÃƒÂÃ†â€™ÃƒÅ½Ã‚Â· Flask bot...")
subprocess.Popen(["python", FLASK_SCRIPT])

print("ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ ÃƒÅ½Ã…Â¸ Lucien ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â¯ÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚Â±ÃƒÅ½Ã‚Â¹ online ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚Â±ÃƒÅ½Ã‚Â¹ ÃƒÂÃ†â€™ÃƒÅ½Ã‚Âµ ÃƒÅ½Ã‚Â±ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚Â¿ÃƒÂÃ‚ÂÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â¹.")





