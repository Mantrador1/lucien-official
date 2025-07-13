import asyncio
from playwright.async_api import async_playwright
import json

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        cookies_path = "playwright_stealth/cookies_ready/wallet1.cookies.json"
        with open(cookies_path, "r", encoding="utf-8-sig") as f:
            cookies = json.load(f)
        await context.add_cookies(cookies)

        page = await context.new_page()
        await page.goto("https://galxe.com", timeout=60000)

        content = await page.content()
        if "Sign in" in content or "login" in content.lower():
            print("❌ Τα cookies ΔΕΝ είναι ενεργά (session expired)")
        else:
            print("✅ Τα cookies είναι ακόμα ενεργά (session OK)")

        await browser.close()

asyncio.run(run())
