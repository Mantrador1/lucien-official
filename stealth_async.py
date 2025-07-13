# stealth.py
from playwright.sync_api import Page
from playwright.async_api import Page as AsyncPage

def stealth_sync(page: Page):
    page.add_init_script("""Object.defineProperty(navigator, 'webdriver', {get: () => undefined})""")
    page.add_init_script("""window.navigator.chrome = { runtime: {} }""")
    page.add_init_script("""Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})""")
    page.add_init_script("""Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})""")

async def stealth_async(page: AsyncPage):
    await page.add_init_script("""Object.defineProperty(navigator, 'webdriver', {get: () => undefined})""")
    await page.add_init_script("""window.navigator.chrome = { runtime: {} }""")
    await page.add_init_script("""Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})""")
    await page.add_init_script("""Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})""")

class Stealth:
    @staticmethod
    def sync(page: Page):
        stealth_sync(page)

    @staticmethod
    async def async_(page: AsyncPage):
        await stealth_async(page)





