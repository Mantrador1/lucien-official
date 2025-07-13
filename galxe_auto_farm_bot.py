import asyncio
from playwright.async_api import async_playwright

urls = [
    "https://app.galxe.com/quest/nibiruchain",
    "https://app.galxe.com/quest/Irys",
    "https://app.galxe.com/quest/Recall"
]

async def farm_galxe():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        for url in urls:
            print(f"🌐 Visiting: {url}")
            await page.goto(url)
            await page.wait_for_timeout(5000)
            try:
                for label in ["Join", "Verify", "Claim"]:
                    button = page.locator(f"button:has-text('{label}')").first
                    if await button.is_visible():
                        print(f"🟢 Clicking: {label}")
                        await button.click()
                        await page.wait_for_timeout(5000)
                        break
            except Exception as e:
                print(f"❌ Error in quest {url}: {e}")
        await browser.close()
        print("✅ Finished Galxe button farm.")

asyncio.run(farm_galxe())





