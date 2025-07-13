from flask import Flask, request, jsonify
from datetime import datetime
import threading

app = Flask(__name__)
AGENTS = {}
SECRET = "supersecrettoken"

def auth_failed(): return jsonify({"error": "unauthorized"}), 403

@app.route('/register', methods=['POST'])
def register():
    if request.headers.get("X-Auth-Token") != SECRET:
        return auth_failed()
    data = request.json
    name = data.get("agent_name")
    if not name: return jsonify({"error": "missing agent_name"}), 400
    AGENTS[name] = {
        "host": data.get("host"),
        "port": data.get("port"),
        "metadata": data.get("metadata", {}),
        "heartbeat_interval": data.get("heartbeat_interval", 30),
        "last_heartbeat": datetime.utcnow().isoformat()
    }
    return jsonify({"status": "success", "message": f"Agent {name} registered"})

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    if request.headers.get("X-Auth-Token") != SECRET:
        return auth_failed()
    data = request.json
    name = data.get("agent_name")
    if name in AGENTS:
        AGENTS[name]["last_heartbeat"] = datetime.utcnow().isoformat()
        return jsonify({"status": "success", "message": "Heartbeat received"})
    return jsonify({"error": "unknown agent"}), 404

@app.route('/agents', methods=['GET'])
def list_agents():
    return jsonify(AGENTS)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000)

@app.route('/dispatch', methods=['POST'])
def dispatch_task():
    if request.headers.get("X-Auth-Token") != SECRET:
        return auth_failed()

    task_data = request.json
    results = {}

    for name, agent in AGENTS.items():
        url = f"http://{agent['host']}:{agent['port']}/task"
        try:
            res = requests.post(url, json=task_data, timeout=10)
            results[name] = res.json()
        except Exception as e:
            results[name] = {"error": str(e)}

    return jsonify(results)





