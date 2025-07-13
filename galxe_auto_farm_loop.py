import json
from playwright.async_api import async_playwright
from playwright_stealth.stealth import Stealth

async def load_cookies(context):
    try:
        with open("cookies.json", "r") as file:
            cookies = json.load(file)
        await context.add_cookies(cookies)
        print("✅ Cookies loaded successfully.")
    except FileNotFoundError:
        print("⚠️ Cookies file not found. Proceeding without cookies.")

async def farm_all_quests():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        await Stealth(context)  # Inject stealth mode
        await load_cookies(context)
        page = await context.new_page()
        await page.goto("https://galxe.com/quests")
        print("🌐 Page loaded. Farming logic goes here.")
        await browser.close()





