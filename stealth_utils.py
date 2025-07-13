import json
from playwright.async_api import async_playwright

async def Stealth(page):
    await page.add_init_script('''
Object.defineProperty(navigator, 'webdriver', {
  get: () => undefined
});
window.navigator.chrome = {
  runtime: {}
};
Object.defineProperty(navigator, 'languages', {
  get: () => ['en-US', 'en']
});
Object.defineProperty(navigator, 'plugins', {
  get: () => [1, 2, 3]
});
    ''')

async def load_cookies(context):
    try:
        with open('cookies.json', 'r') as file:
            cookies = json.load(file)
        await context.add_cookies(cookies)
        print('✅ Cookies loaded successfully.')
    except FileNotFoundError:
        print('⚠️ Cookies file not found. Proceeding without cookies.')

async def farm_logic(page):
    # TODO: Εδώ θα μπει η λογική farming
    print('🌐 Page loaded. Farming logic placeholder.')
    await page.wait_for_timeout(5000)

async def farm_all_quests():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await Stealth(page)
        await load_cookies(context)
        await page.goto('https://galxe.com/quests')
        await farm_logic(page)
        await browser.close()





