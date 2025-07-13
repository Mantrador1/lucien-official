# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime

EMAIL = "fotoniomail@gmail.com"
WALLET = "0x2925b3b18d409ae383339d7f4d753e09eb5f15"

CLAIM_URLS = [
    "https://airdrops.io/visit/a253/",
    "https://airdrops.io/visit/lv43/",
    "https://airdrops.io/visit/8353/",
]

def log_result(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("claims.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def auto_claim(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        print(f"?? Claiming: {url}")
        try:
            page.goto(url, timeout=30000)
            page.wait_for_timeout(3000)

            try:
                page.fill('input[type="email"]', EMAIL)
                print("?? Email filled")
            except PlaywrightTimeoutError:
                print("?? Email input not found")

            try:
                page.fill('input[name="wallet"]', WALLET)
                print("?? Wallet filled")
            except PlaywrightTimeoutError:
                print("?? Wallet input not found")

            try:
                page.click('button[type="submit"]')
                print("? Submit clicked")
            except PlaywrightTimeoutError:
                print("?? Submit button not found")

            page.wait_for_timeout(7000)

            iframes = page.frames
            captcha_frame = None
            for frame in iframes:
                if "captcha" in frame.url.lower():
                    captcha_frame = frame
                    break

            if captcha_frame:
                print("?? CAPTCHA detected! Please solve it manually.")
                input("Press Enter after solving CAPTCHA to continue...")

            print(f"? Claimed at {url}")
            log_result(f"SUCCESS: Claimed at {url}")
        except Exception as e:
            error_msg = f"ERROR at {url}: {e}"
            print(f"? {error_msg}")
            log_result(error_msg)
        finally:
            browser.close()

if __name__ == "__main__":
    for url in CLAIM_URLS:
        auto_claim(url)





