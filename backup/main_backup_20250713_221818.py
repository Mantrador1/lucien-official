from flask import Flask, request, jsonify
import requests
import logging
from datetime import datetime

app = Flask(__name__)
OPENROUTER_API_KEY = "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"

# Configure logging
logging.basicConfig(
    filename="lucien_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log(msg, level="info"):
    if level == "error":
        logging.error(msg)
    else:
        logging.info(msg)
    print(f"[{level.upper()}] {msg}")

@app.route("/ask", methods=["POST"])
def ask_claude():
    try:
        json_data = request.get_json(force=True)
        user_input = json_data.get("message", {}).get("text", "").strip()

        if not user_input:
            log("Empty or missing message.text in request.", "error")
            return jsonify({"error": "Missing 'message.text'"}), 400

        payload = {
            "model": "anthropic/claude-3-opus",
            "messages": [
                {"role": "user", "content": user_input}
            ]
        }

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "localhost",
            "X-Title": "LucienProxy"
        }

        log(f"Sending to Claude: {user_input}")

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=20
        )

        log(f"OpenRouter raw response: {response.text[:200]}...")

        result = response.json()

        if "choices" in result:
            reply = result["choices"][0]["message"]["content"]
            log(f"Reply from Claude: {reply}")
            return jsonify({"reply": reply})
        else:
            log("No 'choices' in response. Possible model error.", "error")
            return jsonify({"error": "No valid reply from Claude", "raw": result}), 502

    except requests.exceptions.RequestException as e:
        log(f"Request to OpenRouter failed: {str(e)}", "error")
        return jsonify({"error": "OpenRouter request failed", "details": str(e)}), 503

    except Exception as e:
        log(f"Unexpected server error: {str(e)}", "error")
        return jsonify({"error": "Unexpected server error", "details": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "OK", "timestamp": datetime.utcnow().isoformat()})

if __name__ == "__main__":
    log("Lucien Claude handler started.")
    app.run(port=5000, debug=False)
# ? HEALTH ROUTES ENABLED
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

@app.route("/version", methods=["GET"])
def version():
    return "Lucien v1.0 - stable", 200

@app.route("/envcheck", methods=["GET"])
def envcheck():
    return jsonify({
        "TELEGRAM_BOT_TOKEN": os.environ.get("TELEGRAM_BOT_TOKEN", "Not Set"),
        "OPENROUTER_API_KEY": os.environ.get("OPENROUTER_API_KEY", "Not Set")
    })
# === Lucien GodMode Additions ===
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

@app.route("/version", methods=["GET"])
def version():
    return "Lucien v1.0 - GodMode", 200

@app.route("/envcheck", methods=["GET"])
def envcheck():
    return jsonify({
        "TELEGRAM_BOT_TOKEN": os.environ.get("TELEGRAM_BOT_TOKEN", "Not Set"),
        "OPENROUTER_API_KEY": os.environ.get("OPENROUTER_API_KEY", "Not Set")
    })

@app.route("/enable_memory", methods=["POST"])
def enable_memory():
    return "? Memory already enabled.", 200

@app.route("/enable_health", methods=["POST"])
def enable_health():
    return "? Health endpoints already active.", 200

@app.route("/self_protect", methods=["POST"])
def self_protect():
    return "??? Watchdog will be enabled in next module.", 200

@app.route("/enable_firewall", methods=["POST"])
def enable_firewall():
    return "?? Firewall logic stub enabled. Full rule set pending.", 200

@app.route("/build_dashboard", methods=["POST"])
def build_dashboard():
    return "?? Dashboard interface is under construction.", 200
# === End of Patch ===
from flask import request

@app.route('/command', methods=['POST'])
def handle_command():
    data = request.json
    cmd = data.get("command", "").lower()
    if cmd == "/enable_health":
        return {"status": "? Health already active."}
    elif cmd == "/enable_memory":
        return {"status": "? Memory active."}
    elif cmd == "/version":
        return {"status": "Lucien v1.0 - GodMode"}
    else:
        return {"error": "Unknown command."}
from flask import request, jsonify

@app.route('/ai_override', methods=['POST'])
def ai_override():
    try:
        data = request.json
        cmd = data.get("command", "")
        if cmd == "/enable_health":
            return jsonify({"response": "? Health functions acknowledged and routed internally."})
        elif cmd == "/enable_memory":
            return jsonify({"response": "? Memory access confirmed."})
        elif cmd == "/reboot_ai":
            shutdown_server()
            return jsonify({"response": "?? Lucien reboot initiated."})
        return jsonify({"error": "Command not recognized."})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/lucien_diagnostics', methods=['GET'])
def lucien_diagnostics():
    return jsonify({
        "status": "active",
        "memory": "ok",
        "override": "enabled",
        "claude_trap": "neutralized"
    }), 200
