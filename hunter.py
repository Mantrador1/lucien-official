import requests, random, time
from datetime import datetime

MAX_RETRIES = 5
DELAY = 4

def load_file(name):
    try:
        with open(name, 'r') as f:
            return [l.strip() for l in f if l.strip()]
    except:
        print(f"[ERROR] Can't read {name}")
        return []

def log(msg):
    with open("log.txt", "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

def claim(wallet, proxy=None):
    url = f"https://airdrop.example.com/claim/{wallet}"  # replace later
    headers = {"User-Agent": random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)"
    ])}
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
    try:
        r = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        if r.status_code == 200 and "success" in r.text.lower():
            print(f"[OK] {wallet} claimed!")
            log(f"SUCCESS: {wallet}")
            return True
        else:
            print(f"[FAIL] {wallet}: Status {r.status_code}")
    except Exception as e:
        print(f"[ERROR] {wallet} with proxy {proxy}: {e}")
    return False

def main():
    wallets = load_file("wallets.txt")
    proxies = load_file("proxies.txt")
    for wallet in wallets:
        success = False
        for attempt in range(MAX_RETRIES):
            proxy = random.choice(proxies) if proxies else None
            print(f"Trying {wallet} using proxy {proxy}...")
            if claim(wallet, proxy):
                success = True
                break
            time.sleep(DELAY)
        if not success:
            print(f"[FAILED] {wallet} after {MAX_RETRIES} attempts.")
            log(f"FAILED: {wallet}")

if __name__ == '__main__':
    main()





