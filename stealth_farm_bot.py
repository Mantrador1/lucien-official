# -*- coding: utf-8 -*-
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            viewport={"width":1280,"height":720},
            locale="en-US",
            timezone_id="Europe/Amsterdam"
        )
        page = await context.new_page()
        await page.goto("https://target-site.com", timeout=60000)
        print("✅ Page loaded (no stealth)")
        # … εδώ βάζεις το farming logic …
        await browser.close()

asyncio.run(main())





