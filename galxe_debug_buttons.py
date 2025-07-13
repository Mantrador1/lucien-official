import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://app.galxe.com")
        await page.wait_for_timeout(20000)  # Περιμένει 20"

        buttons = await page.locator("div[role=button]").all()
        print(f"\n🟣 Found {len(buttons)} buttons:\n")
        for i, btn in enumerate(buttons[:10]):
            try:
                text = await btn.inner_text()
                print(f"Button {i+1}: \"{text.strip()}\"")
            except Exception as e:
                print(f"Button {i+1}: [Error reading text]")

        print("\n🟢 Done. Leaving browser open.")
        await page.wait_for_timeout(15000)  # Κρατά το παράθυρο 15" ανοιχτό

asyncio.run(main())





