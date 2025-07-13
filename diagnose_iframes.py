import asyncio
from playwright.async_api import async_playwright

TARGET_URL = "https://target.com"  # 👉 Βάλε εδώ το πραγματικό URL

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(TARGET_URL)

        frames = page.frames
        print(f"🧩 Found {len(frames)} frames in total:\n")
        for i, frame in enumerate(frames):
            try:
                url = frame.url
                name = frame.name
                print(f"🔹 Frame {i}: name='{name}' url='{url}'")
            except Exception as e:
                print(f"⚠️ Frame {i}: error reading - {e}")

        await asyncio.sleep(15)
        await browser.close()

asyncio.run(main())





