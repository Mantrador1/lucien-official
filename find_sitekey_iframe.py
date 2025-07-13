import asyncio
from playwright.async_api import async_playwright

async def find_sitekey():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto('https://galxe.com/quests')

        # Περιμένουμε λίγο να φορτώσει πιθανό CAPTCHA
        await page.wait_for_timeout(5000)

        # Αναζητούμε σε κύρια σελίδα
        sitekeys_main = await page.eval_on_selector_all('[data-sitekey]', 'els => els.map(e => e.getAttribute("data-sitekey"))')

        # Αναζητούμε σε iframes
        sitekeys_iframes = []
        frames = page.frames
        for frame in frames:
            keys = await frame.eval_on_selector_all('[data-sitekey]', 'els => els.map(e => e.getAttribute("data-sitekey"))')
            sitekeys_iframes.extend(keys)

        sitekeys = list(set(sitekeys_main + sitekeys_iframes))
        if sitekeys:
            print("Found sitekeys:", sitekeys)
        else:
            print("No data-sitekey found in page or iframes.")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(find_sitekey())





