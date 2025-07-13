import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await stealth_async(page)
        await page.goto("https://airdrop-hunter.example.com")
        await page.click("#connectWallet")
        # ... υπόλοιπο farming logic ...
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())





