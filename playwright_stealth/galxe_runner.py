import asyncio
from playwright.async_api import async_playwright
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('--wallet', required=True)
parser.add_argument('--cookie', required=True)
args = parser.parse_args()

async def run(wallet_address, cookie_path):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        # Load cookies if they exist
        try:
            with open(cookie_path, 'r') as f:
                cookies = json.load(f)
                await context.add_cookies(cookies)
        except Exception as e:
            print(f"[{wallet_address}] WARNING Failed to load cookies: {e}")

        page = await context.new_page()

        # Navigate to Galxe
        await page.goto("https://galxe.com", timeout=60000)
        print(f"[{wallet_address}]  Page loaded.")

        # Example interaction (you can customize this)
        await page.wait_for_timeout(5000)

        await browser.close()

asyncio.run(run(args.wallet, args.cookie))

