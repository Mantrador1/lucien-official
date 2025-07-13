from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)
AUTH_TOKEN = 'your_shared_secret_token'

@app.route('/task', methods=['POST'])
def task():
    token = request.headers.get('X-Auth-Token')
    if token != AUTH_TOKEN:
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    try:
        data = request.get_json()
        task_type = data.get("task")
        payload = data.get("data")
        print(f"[{datetime.datetime.now().isoformat()}] ✅ Received task: {task_type} | Data: {payload}")
        # εδώ μπορεί να προστεθεί η επεξεργασία task
        return jsonify({"status": "success", "message": f"Task '{task_type}' processed"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5050)





