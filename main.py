from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

TELEGRAM_CHAT_ID = os.getenv("CHAT_ID")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = "anthropic/claude-3-opus"

def send_telegram_message(message):
    if not TELEGRAM_CHAT_ID or not TELEGRAM_BOT_TOKEN:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = { "chat_id": TELEGRAM_CHAT_ID, "text": message }
    try { requests.post(url, data=data) } catch {}

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({ "error": "Missing 'message' field" }), 400

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = @{
        "model" = OPENROUTER_MODEL
        "messages" = @(@{ "role" = "user"; "content" = $user_message })
        "temperature" = 0.7
    }
    try {
        $response = Invoke-RestMethod -Uri "https://openrouter.ai/api/v1/chat/completions" -Method Post -Headers $headers -Body ($payload | ConvertTo-Json -Depth 3)
        $reply = $response.choices[0].message.content
        send_telegram_message "🤖 Lucien:`n$reply"
        return $reply
    } catch {
        send_telegram_message "❌ Error: $($_.Exception.Message)"
        return "Error"
    }

@app.route('/health')
def health(): return "OK", 200

@app.route('/envcheck')
def envcheck(): return jsonify({
    "CHAT_ID": TELEGRAM_CHAT_ID,
    "BOT_TOKEN_SET": bool(TELEGRAM_BOT_TOKEN),
    "OPENROUTER_KEY_SET": bool(OPENROUTER_API_KEY)
})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
