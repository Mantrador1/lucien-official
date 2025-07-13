import os
import asyncio
import requests
from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv()
CAPSOLVER_API_KEY = os.getenv("CAPSOLVER_API_KEY")
TARGET_URL = "https://target.com"  # 👉 Βάλε εδώ το πραγματικό URL

async def extract_sitekey(page):
    await page.goto(TARGET_URL)
    await page.wait_for_selector("iframe[src*='turnstile']", timeout=15000)
    frame_element = await page.query_selector("iframe[src*='turnstile']")
    sitekey = await frame_element.get_attribute("data-sitekey")
    return sitekey

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        sitekey = await extract_sitekey(page)
        if not sitekey:
            print("❌ Δεν βρέθηκε sitekey στο iframe.")
            await browser.close()
            return

        print(f"✅ Sitekey: {sitekey}")

        payload = {
            "clientKey": CAPSOLVER_API_KEY,
            "task": {
                "type": "AntiTurnstileTaskProxyLess",
                "websiteKey": sitekey,
                "websiteURL": TARGET_URL
            }
        }
        res = requests.post("https://api.capsolver.com/createTask", json=payload).json()
        task_id = res.get("taskId")

        token = None
        for _ in range(30):
            result = requests.post("https://api.capsolver.com/getTaskResult", json={
                "clientKey": CAPSOLVER_API_KEY,
                "taskId": task_id
            }).json()
            if result.get("status") == "ready":
                token = result["solution"]["token"]
                break
            await asyncio.sleep(2)

        if not token:
            print("❌ Το CapSolver απέτυχε.")
            await browser.close()
            return

        await page.evaluate("""(token) => {
            const el = document.querySelector('input[name="cf-turnstile-response"]');
            if (el) {
                el.value = token;
                el.dispatchEvent(new Event('change', { bubbles: true }));
            }
            if (window.tsCallback) {
                window.tsCallback(token);
            }
        }""", token)

        try:
            await page.click('button[type="submit"]')
        except:
            print("⚠️ Δεν βρέθηκε κουμπί submit")

        await asyncio.sleep(10)
        await browser.close()

asyncio.run(main())





