@app.route("/ask", methods=["POST"])
def ask():
    data = json.loads(request.data)
    print("📩 RECEIVED PAYLOAD:", data)
    prompt = data.get("prompt", "")
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "claude-3-opus",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    result = response.json()
    return jsonify(result)




