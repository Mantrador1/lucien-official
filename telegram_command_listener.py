import requests
import subprocess
import time

# === ΡΥΘΜΙΣΕΙΣ ===
TOKEN = "7573715897:AAGgNmOxIOrRywzihuF4jFYkBTU9ymvwgn0"
CHAT_ID = 670585523  # χωρίς εισαγωγικά, αριθμός

URL = f"https://api.telegram.org/bot{TOKEN}/"
last_update_id = 0

def send_message(text):
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(URL + "sendMessage", data=data)

def get_updates():
    global last_update_id
    try:
        params = {"offset": last_update_id + 1, "timeout": 10}
        response = requests.get(URL + "getUpdates", params=params)
        result = response.json()["result"]
        return result
    except Exception as e:
        print("Σφάλμα στο get_updates:", e)
        return []

def execute_command(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return e.output.decode("utf-8")
    except Exception as e:
        return f"Σφάλμα: {str(e)}"

# === MAIN LOOP ===
print("🛰 Lucien Command Listener ενεργός.")
send_message("🛰 Lucien Command Listener ενεργός.")

while True:
    updates = get_updates()
    for update in updates:
        last_update_id = update["update_id"]
        message = update.get("message", {})
        text = message.get("text", "")
        sender_id = message.get("from", {}).get("id", 0)

        print(f"[{sender_id}] -> {text}")  # DEBUG

        if sender_id != CHAT_ID:
            send_message("⛔ Άρνηση πρόσβασης.")
            continue

        if not text:
            continue

        result = execute_command(text)
        if not result.strip():
            result = "✅ Εντολή εκτελέστηκε χωρίς έξοδο."
        elif len(result) > 4000:
            result = result[:4000] + "\n...απάντηση περικόπηκε."

        send_message(f"📤 Απάντηση:\n{result}")
    time.sleep(2)
