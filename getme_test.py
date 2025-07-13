# -*- coding: utf-8 -*-
import requests

TOKEN = "1837395252:AAHvPLfJECS5zGvFuYjeBEFmwGm5g0HSq0I"

def get_me():
    url = f"https://api.telegram.org/bot{TOKEN}/getMe"
    response = requests.get(url)
    print(response.status_code)
    print(response.json())

get_me()





