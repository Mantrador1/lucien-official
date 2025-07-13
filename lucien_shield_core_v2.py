# -*- coding: utf-8 -*-
import telebot
import subprocess
import pyautogui
import os
import pyperclip
import datetime
import threading
import time
import socket
import sounddevice as sd
import speech_recognition as sr
from pystray import Icon, MenuItem as item, Menu
from PIL import Image, ImageDraw

# -- CONFIG
CHAT_ID = os.getenv("CHAT_ID")
TOKEN = os.environ.get("BOT_TOKEN")
PIN_CODE = "360"
BASE_PATH = os.getcwd()
UPLOAD_FOLDER = os.path.join(BASE_PATH, "uploads")
LOG_FOLDER = os.path.join(BASE_PATH, "logs")
CHECK_INTERVAL = 3600
INACTIVITY_HOURS = 24

# -- INIT
bot = telebot.TeleBot(TOKEN)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

last_command_time = time.time()
icon_instance = None
previous_ip = None

# == FUNCTIONS ==

def log_action(text):
    global last_command_time
    last_command_time = time.time()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    filename = datetime.datetime.now().strftime('commands_%Y-%m-%d.log')
    with open(os.path.join(LOG_FOLDER, filename), 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {text}\n")

def format_size(size):
    return f"{size / (1024*1024):.1f} MB" if size > 1024*1024 else f"{size / 1024:.1f} KB"

def format_date(ts):
    return datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M')

def scan_folder(path):
    if not os.path.exists(path):
        return "ÃƒÂ¢Ã‚ÂÃ…â€™ ÃƒÅ½Ã…Â¸ ÃƒÂÃ¢â‚¬Â ÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Â¿ÃƒÂÃ¢â‚¬Å¡ ÃƒÅ½Ã‚Â´ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â½ ÃƒÂÃ¢â‚¬Â¦ÃƒÂÃ¢â€šÂ¬ÃƒÅ½Ã‚Â¬ÃƒÂÃ‚ÂÃƒÂÃ¢â‚¬Â¡ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â¹."
    try:
        entries = os.listdir(path)
        if not entries:
            return "ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã¢â‚¬Å¡ ÃƒÅ½Ã…Â¸ ÃƒÂÃ¢â‚¬Â ÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Â¿ÃƒÂÃ¢â‚¬Å¡ ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â¯ÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚Â±ÃƒÅ½Ã‚Â¹ ÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚Â´ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â¹ÃƒÅ½Ã‚Â¿ÃƒÂÃ¢â‚¬Å¡."
        lines = [f"ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã‚Â {path}"]
        for entry in entries:
            full = os.path.join(path, entry)
            if os.path.isfile(full):
                size = os.path.getsize(full)
                date = os.path.getmtime(full)
                lines.append(f"- {entry} | {format_size(size)} | {format_date(date)}")
        return "\n".join(lines)
    except Exception as e:
        return f"ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â ÃƒÅ½Ã‚Â£ÃƒÂÃ¢â‚¬Â ÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Â± ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚Â±ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â¬ ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â¿ scan: {str(e)}"

def execute_command(command):
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return f"ÃƒÂ¢Ã‚ÂÃ…â€™ ÃƒÅ½Ã‚Â£ÃƒÂÃ¢â‚¬Â ÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Â±:\n{e.output}"
    except Exception as e:
        return f"ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â ÃƒÅ½Ã¢â‚¬Â¢ÃƒÅ½Ã‚Â¾ÃƒÅ½Ã‚Â±ÃƒÅ½Ã‚Â¯ÃƒÂÃ‚ÂÃƒÅ½Ã‚ÂµÃƒÂÃ†â€™ÃƒÅ½Ã‚Â·:\n{str(e)}"
def take_screenshot():
    try:
        path = os.path.join(BASE_PATH, "screen.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        return path
    except Exception:
        return None

def send_file(path, chat_id):
    try:
        if not os.path.exists(path):
            return False
        with open(path, 'rb') as f:
            bot.send_document(chat_id, f)
        return True
    except Exception:
        return False

def check_inactivity():
    while True:
        time.sleep(CHECK_INTERVAL)
        delta_hours = (time.time() - last_command_time) / 3600
        if delta_hours >= INACTIVITY_HOURS:
            today = datetime.datetime.now().strftime('commands_%Y-%m-%d.log')
            log_path = os.path.join(LOG_FOLDER, today)
            sent_flag = log_path + ".sent"
            if os.path.exists(log_path) and not os.path.exists(sent_flag):
                try:
                    with open(log_path, 'rb') as f:
                        bot.send_document(CHAT_ID, f, caption="ÃƒÂ°Ã…Â¸Ã¢â‚¬Â¢Ã¢â‚¬Å“ 24h inactivity ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“ ÃƒÅ½Ã‚Â±ÃƒÂÃ¢â‚¬Â¦ÃƒÂÃ¢â‚¬Å¾ÃƒÂÃ…â€™ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Â±ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â¿ log")
                    open(sent_flag, 'w').close()
                except:
                    pass

def watch_network():
    global previous_ip
    while True:
        try:
            ip = socket.gethostbyname(socket.gethostname())
            if previous_ip and ip != previous_ip:
                bot.send_message(CHAT_ID, f"ÃƒÂ°Ã…Â¸Ã…â€™Ã‚Â ÃƒÅ½Ã‚ÂÃƒÅ½Ã‚Â­ÃƒÅ½Ã‚Â± IP ÃƒÅ½Ã‚Â±ÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚Â¹ÃƒÂÃ¢â‚¬Â¡ÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚ÂµÃƒÂÃ‚ÂÃƒÅ½Ã‚Â¸ÃƒÅ½Ã‚Â·ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚Âµ: {ip}")
                log_action(f"IP ÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Â±ÃƒÅ½Ã‚Â¾ÃƒÅ½Ã‚Âµ: {previous_ip} ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ {ip}")
            previous_ip = ip
        except:
            pass
        time.sleep(180)
def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    while True:
        try:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio, language='el-GR')
            if command:
                log_action(f"ÃƒÂ°Ã…Â¸Ã…Â½Ã¢â€žÂ¢ÃƒÂ¯Ã‚Â¸Ã‚Â ÃƒÅ½Ã‚Â¦ÃƒÂÃ¢â‚¬Â°ÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚Â®: {command}")
                output = execute_command(command)
                if output:
                    bot.send_message(CHAT_ID, f"ÃƒÂ°Ã…Â¸Ã¢â‚¬â€Ã‚Â£ÃƒÂ¯Ã‚Â¸Ã‚Â {command}\nÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã‚Â¤ {output[:4000]}")
        except sr.UnknownValueError:
            continue
        except:
            time.sleep(5)

def create_icon():
    image = Image.new('RGB', (64, 64), (255, 0, 0))
    d = ImageDraw.Draw(image)
    d.rectangle((8, 8, 56, 56), fill=(0, 0, 0))
    return image

def show_status(icon, item):
    log_action("Tray: Show status clicked.")
    os.startfile(LOG_FOLDER)

def send_log_now(icon, item):
    try:
        today = datetime.datetime.now().strftime('commands_%Y-%m-%d.log')
        log_path = os.path.join(LOG_FOLDER, today)
        if os.path.exists(log_path):
            with open(log_path, 'rb') as f:
                bot.send_document(CHAT_ID, f, caption="ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã‚Â ÃƒÅ½Ã‚Â§ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â¹ÃƒÂÃ‚ÂÃƒÅ½Ã‚Â¿ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚Â¯ÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚Â·ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â· ÃƒÅ½Ã‚Â±ÃƒÂÃ¢â€šÂ¬ÃƒÅ½Ã‚Â¿ÃƒÂÃ†â€™ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â¿ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Â® log")
    except:
        pass

def tray():
    global icon_instance
    icon_instance = Icon("Lucien", create_icon(), "Lucien", menu=Menu(
        item('ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã‚Â¤ Send Log Now', send_log_now),
        item('ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã‚Â Show Status', show_status),
        item('ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ¢â‚¬â„¢ Exit (PIN ÃƒÅ½Ã‚Â¼ÃƒÂÃ…â€™ÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚Â¿)', lambda icon, item: None)
    ))
    icon_instance.run()
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global icon_instance
    if message.chat.id != CHAT_ID:
        return

    command = message.text.strip()
    log_action(f"Command received: {command}")

    if command.startswith("/pin "):
        entered_pin = command[5:].strip()
        if entered_pin == PIN_CODE:
            bot.send_message(message.chat.id, "ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Â PIN OK. ÃƒÅ½Ã‚Â¤ÃƒÅ½Ã‚ÂµÃƒÂÃ‚ÂÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Â±ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â¹ÃƒÂÃ†â€™ÃƒÅ½Ã‚Â¼ÃƒÂÃ…â€™ÃƒÂÃ¢â‚¬Å¡ Lucien...")
            log_action("Lucien exited via PIN.")
            if icon_instance:
                icon_instance.stop()
            os._exit(0)
        else:
            bot.send_message(message.chat.id, "ÃƒÂ¢Ã‚ÂÃ…â€™ ÃƒÅ½Ã¢â‚¬ÂºÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚Â¸ÃƒÅ½Ã‚Â¿ÃƒÂÃ¢â‚¬Å¡ PIN.")
        return

    if command == "/screenshot":
        path = take_screenshot()
        if path:
            with open(path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
            os.remove(path)
            log_action("Screenshot sent.")
        return

    if command.startswith("/get "):
        filename = command[5:].strip()
        if send_file(filename, message.chat.id):
            bot.send_message(message.chat.id, f"ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã…Â½ ÃƒÅ½Ã¢â‚¬ËœÃƒÂÃ¢â€šÂ¬ÃƒÅ½Ã‚ÂµÃƒÂÃ†â€™ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Â·: {filename}")
            log_action(f"File sent: {filename}")
        else:
            bot.send_message(message.chat.id, f"ÃƒÂ¢Ã‚ÂÃ…â€™ ÃƒÅ½Ã¢â‚¬ÂÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â½ ÃƒÅ½Ã‚Â²ÃƒÂÃ‚ÂÃƒÅ½Ã‚Â­ÃƒÅ½Ã‚Â¸ÃƒÅ½Ã‚Â·ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚Âµ: {filename}")
        return

    if command.startswith("/scan "):
        folder = command[6:].strip()
        result = scan_folder(folder)
        bot.send_message(message.chat.id, result)
        return

    if command == "/clip":
        try:
            clip = pyperclip.paste()
            bot.send_message(message.chat.id, f"ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã¢â‚¬Â¹ Clipboard:\n{clip}")
            log_action("Clipboard sent.")
        except Exception as e:
            bot.send_message(message.chat.id, f"ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â Clipboard error: {str(e)}")
        return

    if command == "/startup":
        try:
            result = execute_command("wmic startup get Caption, Command")
            bot.send_message(message.chat.id, f"ÃƒÂ°Ã…Â¸Ã…Â¡Ã¢â€šÂ¬ ÃƒÅ½Ã¢â‚¬Â¢ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚Â¯ÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚Â·ÃƒÂÃ†â€™ÃƒÅ½Ã‚Â·:\n{result}")
        except:
            pass
        return

# -- LAUNCH EVERYTHING --
threading.Thread(target=bot.polling, daemon=True).start()
threading.Thread(target=tray, daemon=True).start()
threading.Thread(target=watch_network, daemon=True).start()
threading.Thread(target=check_inactivity, daemon=True).start()
threading.Thread(target=recognize_speech, daemon=True).start()

while True:
    time.sleep(1)





