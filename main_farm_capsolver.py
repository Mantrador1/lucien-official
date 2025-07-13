import asyncio
import json
from playwright.async_api import async_playwright
from capsolver_integration import CapSolver

API_KEY = 'sk-your-real-capsolver-api-key'  # Εδώ βάζω εγώ το δικό σου
SITE_KEY = 'site_key_from_galxe_or_target'  # Θα βρούμε μαζί το σωστό site key
SITE_URL = 'https://galxe.com/quests'

async def Stealth(page):
    await page.add_init_script('''
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
window.navigator.chrome = { runtime: {} };
Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
    ''')

async def load_cookies(context):
    try:
        with open('cookies.json', 'r') as file:
            cookies = json.load(file)
        await context.add_cookies(cookies)
        print('✅ Cookies loaded successfully.')
    except FileNotFoundError:
        print('⚠️ Cookies file not found. Proceeding without cookies.')

async def solve_captcha_and_fill(page):
    solver = CapSolver(API_KEY)
    token = await solver.solve_turnstile(SITE_KEY, SITE_URL)
    print(f'🧩 CAPTCHA solved, token: {token}')
    # Εδώ θα βάλουμε το token στη σελίδα (θα το υλοποιήσουμε)

async def farm_all_quests():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await Stealth(page)
        await load_cookies(context)
        await page.goto(SITE_URL)
        await solve_captcha_and_fill(page)
        # TODO: Λογική claim quests
        await asyncio.sleep(10)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(farm_all_quests())





