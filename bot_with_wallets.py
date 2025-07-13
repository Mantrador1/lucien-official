import asyncio
import json
from playwright.async_api import async_playwright
from cryptography.fernet import Fernet

PROXIES = []
try:
    from proxies_list import PROXIES
except ImportError:
    pass

def load_wallets(filename, key):
    fernet = Fernet(key)
    with open(filename, 'rb') as f:
        encrypted = f.read()
    decrypted = fernet.decrypt(encrypted)
    return json.loads(decrypted.decode())

async def stealth_setup(page):
    await page.add_init_script('''
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
window.navigator.chrome = { runtime: {} };
Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
''')

async def farm_task(page, wallet):
    # TODO: Υλοποίησε farming λογική εδώ
    await asyncio.sleep(5)
    print(f'Farming done for wallet {wallet["address"]}')

async def run_bot(wallet, proxy):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, proxy={"server": proxy} if proxy else None)
        context = await browser.new_context()
        page = await context.new_page()
        await stealth_setup(page)
        await farm_task(page, wallet)
        await browser.close()

async def main():
    with open('wallet_key.key', 'rb') as f:
        key = f.read()

    wallets = load_wallets('wallets.enc', key)

    tasks = []
    for i, wallet in enumerate(wallets):
        proxy = PROXIES[i % len(PROXIES)] if PROXIES else None
        tasks.append(run_bot(wallet, proxy))
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())





