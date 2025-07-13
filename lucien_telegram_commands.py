import requests, time, subprocess, os
import urllib3
urllib3.disable_warnings()

BOT_TOKEN = "7121107982:AAHEs4EGv57F2J3kI8AxFeTKHFY5hgq8yX8"
CHAT_ID = "5370071479"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
LOG_PATH = "C:/lucien_proxy/logs/command_debug.log"
LAST_UPDATE_ID = None

def log(msg):
    print(msg)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"{time.ctime()} :: {msg}\n")

def send_message(text):
    try:
        r = requests.post(f"{API_URL}/sendMessage", data={"chat_id": CHAT_ID, "text": text}, verify=False)
        log(f"Sent message: {text} | Response: {r.status_code}")
    except Exception as e:
        log(f"Error sending message: {e}")

def handle_command(text):
    try:
        if text == "/status":
            tasks = subprocess.check_output("tasklist", shell=True).decode()
            msg = " Lucien Status:\n"
            msg += "main.py:  running\n" if "main.py" in tasks else "main.py:  not running\n"
            msg += "telegram_listener.py:  running\n" if "telegram_listener.py" in tasks else "telegram_listener.py:  not running\n"
            msg += "laptop_link.ps1:  maybe\n" if "powershell.exe" in tasks and "laptop_link" in tasks else "laptop_link.ps1:  not running\n"
            send_message(msg)
        elif text == "/restart":
            subprocess.call('taskkill /f /im python.exe', shell=True)
            time.sleep(1)
            subprocess.Popen(["python", "main.py"])
            subprocess.Popen(["python", "telegram_listener.py"])
            send_message(" Lucien restarted.")
        elif text == "/kill":
            subprocess.call('taskkill /f /im python.exe', shell=True)
            send_message(" All Lucien processes killed.")
        elif text == "/log":
            msg = ""
            for fname in ["updater.log", "watchdog.log"]:
                path = f"C:/lucien_proxy/logs/{fname}"
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        lines = f.readlines()[-5:]
                        msg += f" {fname}:\n{''.join(lines)}\n"
                else:
                    msg += f" {fname} not found\n"
            send_message(msg)
        else:
            send_message(" Unknown command.")
    except Exception as e:
        log(f"Error in handle_command: {e}")

while True:
    try:
        r = requests.get(f"{API_URL}/getUpdates", timeout=5, verify=False)
        updates = r.json()
        if "result" in updates:
            for update in updates["result"]:
                uid = update["update_id"]
                if uid != LAST_UPDATE_ID:
                    LAST_UPDATE_ID = uid
                    msg = update.get("message", {}).get("text", "")
                    log(f"Received command: {msg}")
                    if msg.startswith("/"):
                        handle_command(msg.strip())
    except Exception as e:
        log(f"Polling error: {e}")
    time.sleep(2)
