import json
from datetime import datetime

SCORE_FILE = 'score.json'
LOG_FILE = 'log.txt'

def save_scores(scores):
    with open(SCORE_FILE, 'w', encoding='utf-8') as f:
        json.dump(scores, f, indent=2)

def load_scores():
    try:
        with open(SCORE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {'gpt4': 1.0, 'claude': 1.0}

def log_error(model, prompt, error):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{datetime.now().isoformat()}] ? Model: {model} | Error: {error} | Prompt: {prompt}\n")





