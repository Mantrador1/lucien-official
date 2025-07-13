from playwright.async_api import async_playwright

class StealthBrowser:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def launch(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        await self.page.add_init_script("""Object.defineProperty(navigator, 'webdriver', {get: () => undefined})""")
        await self.page.set_extra_http_headers({"Accept-Language": "en-US,en;q=0.9"})
        await self.page.goto("https://galxe.com", timeout=60000)

    async def close(self):
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()





