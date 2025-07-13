import asyncio
import os
from pathlib import Path
from stealth import StealthBrowser
from galxe_auto_farm_loop import load_cookies

async def scan_quests(browser, cookie_file):
    await load_cookies(browser.page, cookie_file)
    print("✅ Cookies loaded")
    await browser.page.goto("https://app.galxe.com/me/quest", timeout=60000)
    await browser.page.wait_for_timeout(5000)
    quests = await browser.page.query_selector_all("div[class*=questCard]")
    print(f"🧩 Found {len(quests)} quests")
    for quest in quests:
        title = await quest.inner_text()
        print("➡️", title.strip().split("\n")[0])
    await browser.close()

async def main():
    cookies_dir = Path("cookies")
    for cookie_file in cookies_dir.glob("*.txt"):
        print(f"\n🌐 Scanning for: {cookie_file}")
        browser = StealthBrowser()
        await browser.launch()
        await scan_quests(browser, str(cookie_file))

if __name__ == "__main__":
    asyncio.run(main())





