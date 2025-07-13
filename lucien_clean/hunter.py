import requests, time, random

WALLETS_FILE = "wallets.txt"
PROXIES_FILE = "proxies.txt"
CLAIM_URL = "https://claim.newt.network/api/claim"
MAX_RETRIES = 3

def load_wallets():
    with open(WALLETS_FILE) as f:
        return [line.strip() for line in f if line.strip()]

def load_proxies():
    with open(PROXIES_FILE) as f:
        return [line.strip() for line in f if line.strip()]

def send_claim(wallet, proxy=None):
    try:
        session = requests.Session()
        if proxy:
            session.proxies = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }
        response = session.post(CLAIM_URL, json={"wallet": wallet}, timeout=15)
        if response.ok:
            print(f"[? SUCCESS] {wallet}: {response.json()}")
            return True
        else:
            print(f"[? FAIL] {wallet}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[?? ERROR] {wallet} with proxy {proxy}: {e}")
    return False

def main():
    wallets = load_wallets()
    proxies = load_proxies()
    for wallet in wallets:
        attempt = 0
        success = False
        while attempt < MAX_RETRIES and not success:
            proxy = random.choice(proxies) if proxies else None
            print(f"Trying {wallet} using proxy {proxy}...")
            success = send_claim(wallet, proxy)
            if not success:
                time.sleep(5)
            attempt += 1
        if not success:
            print(f"[? FAILED] {wallet} after {MAX_RETRIES} attempts.")

if __name__ == "__main__":
    main()





