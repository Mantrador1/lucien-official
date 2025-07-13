# -*- coding: utf-8 -*-
import os
import requests

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

if TELEGRAM_TOKEN:
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getMe"
    try:
        response = requests.get(url)
        print(f'Status Code: {response.status_code}')
        print(response.json())
    except Exception as e:
        print(f'Error during request: {e}')
else:
    print('Error: TELEGRAM_TOKEN environment variable is not set.')





