import os, requests, time, traceback

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

def send_message(text):
    print(f"📤 Sending to Telegram: {text}")
    try:
        requests.post(f"{API_URL}/sendMessage", json={"chat_id": CHAT_ID, "text": text})
    except Exception as e:
        print(f"❌ Telegram send failed: {e}")

def get_claude_response(user_message):
    print(f"🤖 Asking Claude: {user_message}")
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://yourdomain.com",
        "X-Title": "LucienTelegram"
    }
    payload = {
        "model": "anthropic/claude-3-opus",
        "messages": [{"role": "user", "content": user_message}]
    }
    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                          headers=headers, json=payload, timeout=60)
        print("📦 Claude raw response:", r.text)
        result = r.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ Claude error:", traceback.format_exc())
        return f"⚠️ Claude Error: {e}"

def get_updates(offset=None):
    params = {"timeout": 100, "offset": offset}
    r = requests.get(f"{API_URL}/getUpdates", params=params)
    return r.json().get("result", [])

def main():
    print("🚀 Claude Telegram Bot LIVE")
    last_update_id = None
    send_message("🤖 Claude Lucien ενεργοποιήθηκε (debug mode)")
    while True:
        try:
            updates = get_updates(last_update_id)
            for update in updates:
                last_update_id = update["update_id"] + 1
                message = update.get("message", {}).get("text", "")
                chat_id = update.get("message", {}).get("chat", {}).get("id", "")
                print(f"📥 From {chat_id}: {message}")
                if str(chat_id) != CHAT_ID:
                    send_message("❌ Unauthorized user.")
                    continue
                if message:
                    reply = get_claude_response(message)
                    send_message(reply)
        except Exception as e:
            print("🛑 Loop error:", traceback.format_exc())
            time.sleep(5)

if __name__ == "__main__":
    main()
