from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ Lucien Proxy is alive!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Received data:", data)
    return "Webhook received", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

