import json
import os
from adapters.gpt4 import call_gpt4
from adapters.claude import call_claude
from adapters.shadow_mistral import call_shadow_mistral

SCORE_FILE = './score.json'

def load_scores():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, 'r') as f:
            return json.load(f)
    return {'gpt4': 1.0, 'claude': 1.0}

def save_scores(scores):
    with open(SCORE_FILE, 'w') as f:
        json.dump(scores, f)

def log_error(model, prompt, error):
    with open('errors.log', 'a') as f:
        f.write(f'[{model}] Error for prompt \"{prompt}\": {error}\\n')

def route_request(prompt):
    scores = load_scores()
    models = sorted(scores, key=scores.get, reverse=True)

    for model in models:
        try:
            if model == 'gpt4':
                response = call_gpt4(prompt)
            elif model == 'claude':
                response = call_claude(prompt)
            else:
                continue

            if 'I can�t' in response or 'I�m afraid' in response or 'I won�t' in response:
                log_error(model, prompt, 'Refused task')
                scores[model] = max(scores.get(model, 1.0) - 0.5, 0.1)
                save_scores(scores)
                continue

            save_scores(scores)
            return response

        except Exception as e:
            log_error(model, prompt, str(e))
            scores[model] = max(scores.get(model, 1.0) - 0.2, 0.1)
            save_scores(scores)

    try:
        return call_shadow_mistral(prompt)
    except Exception as e:
        return f'? Shadow fallback failed: {str(e)}'





