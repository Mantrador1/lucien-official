import os
import time
import requests

def main():
    while True:
        prompt = "List all stealth automation steps needed to farm Galxe and Zealy quests efficiently using Playwright in Python. Include evasion logic, rotation, and multi-account handling."

        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post("http://127.0.0.1:8080/ask", json={"prompt": prompt}, headers=headers)
            print("\n?? Claude:\n", response.text)
        except Exception as e:
            print("? Error:", e)

        time.sleep(30)

if __name__ == "__main__":
    main()




