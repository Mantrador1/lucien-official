from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Lucien Proxy is active!'

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
