import requests
import os

def call_claude(prompt):
    try:
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {os.getenv("OPENROUTER_API_KEY")}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'anthropic/claude-3-opus',
                'messages': [{'role': 'user', 'content': prompt}]
            }
        )
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f'? Claude error: {str(e)}'





