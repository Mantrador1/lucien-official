import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://app.galxe.com")
        await page.wait_for_timeout(15000)  # Περιμένει 15"

        print("\n🔵 BUTTONS:")
        buttons = await page.locator("button").all()
        for i, btn in enumerate(buttons[:15]):
            try:
                text = await btn.inner_text()
                print(f"Button {i+1}: \"{text.strip()}\"")
            except:
                print(f"Button {i+1}: [Unreadable]")

        print("\n🔵 LINKS (a[href]):")
        links = await page.locator("a[href]").all()
        for i, link in enumerate(links[:15]):
            try:
                href = await link.get_attribute("href")
                text = await link.inner_text()
                print(f"Link {i+1}: \"{text.strip()}\" -> {href}")
            except:
                print(f"Link {i+1}: [Unreadable]")

        await page.wait_for_timeout(15000)  # Κρατάει ανοιχτό 15"

asyncio.run(main())





