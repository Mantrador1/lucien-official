import asyncio
from playwright.async_api import async_playwright

async def farm_galxe():
    quests = [
        "https://app.galxe.com/quest/nibiruchain",
        "https://app.galxe.com/quest/Irys",
        "https://app.galxe.com/quest/Recall"
    ]
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://app.galxe.com")
        await page.wait_for_timeout(8000)

        for url in quests:
            print(f"\n🌐 Visiting: {url}")
            await page.goto(url)
            await page.wait_for_timeout(15000)  # Περιμένει 15"

        print("✅ Done farming Galxe!")
        await browser.close()

asyncio.run(farm_galxe())





