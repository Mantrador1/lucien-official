import asyncio
from playwright.async_api import async_playwright

async def find_sitekey():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto('https://galxe.com/quests')
        # Αναζήτηση δυναμικά για στοιχεία με data-sitekey attribute
        sitekeys = await page.eval_on_selector_all('[data-sitekey]', 'elements => elements.map(e => e.getAttribute("data-sitekey"))')
        if sitekeys:
            print('Found sitekeys:', sitekeys)
        else:
            print('No data-sitekey found on the page.')
        await browser.close()

if __name__ == "__main__":
    asyncio.run(find_sitekey())





