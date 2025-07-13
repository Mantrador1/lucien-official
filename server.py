# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Lucien Proxy is alive'

@app.route('/command', methods=['POST'])
def command():
    data = request.get_json()
    if not data or 'command' not in data:
        return jsonify({'error': 'No command provided'}), 400

    cmd = data['command']
    try:
        # Execute the command and capture output
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
        return jsonify({'output': result})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': e.output}), 500

if __name__ == '__main__':
    from waitress import serve
    port = int(os.environ.get("PORT", 8080))
    serve(app, host='0.0.0.0', port=port)





