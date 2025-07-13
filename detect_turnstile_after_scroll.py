import asyncio
from playwright.async_api import async_playwright

TARGET_URL = "https://www.target.com"  # 👉 Βάλε το πραγματικό URL

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=100)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(TARGET_URL)

        print("🖱️ Κάνε scroll/click χειροκίνητα αν χρειάζεται για να εμφανιστεί το CAPTCHA...")
        await asyncio.sleep(20)  # ⏱️ Περιθώριο για αλληλεπίδραση

        frames = page.frames
        print(f"\n🧩 Found {len(frames)} frames after interaction:\n")
        for i, frame in enumerate(frames):
            try:
                print(f"🔹 Frame {i}: name='{frame.name}' url='{frame.url}'")
            except Exception as e:
                print(f"⚠️ Frame {i}: error reading - {e}")

        await browser.close()

asyncio.run(main())





