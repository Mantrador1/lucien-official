import aiohttp
import asyncio

class CapSolver:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = 'https://api.capsolver.com'

    async def submit_turnstile(self, site_key, site_url):
        payload = {
            'clientKey': self.api_key,
            'task': {
                'type': 'TurnstileTask',
                'websiteURL': site_url,
                'websiteKey': site_key,
                'isInvisible': True
            }
        }
        print(f'Submitting task with payload: {payload}')
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{self.api_url}/createTask', json=payload) as resp:
                print(f'Response status: {resp.status}')
                resp_text = await resp.text()
                print(f'Response text: {resp_text}')
                resp.raise_for_status()
                data = await resp.json()
                return data.get('taskId')

    async def get_result(self, task_id, max_wait=120, interval=5):
        payload = {
            'clientKey': self.api_key,
            'taskId': task_id
        }
        async with aiohttp.ClientSession() as session:
            for _ in range(0, max_wait, interval):
                await asyncio.sleep(interval)
                async with session.post(f'{self.api_url}/getTaskResult', json=payload) as resp:
                    print(f'Checking result status: {resp.status}')
                    resp_text = await resp.text()
                    print(f'Response text: {resp_text}')
                    resp.raise_for_status()
                    data = await resp.json()
                    if data.get('status') == 'ready':
                        return data['solution']['token']
            raise TimeoutError('CAPTCHA solving timed out')

    async def solve_turnstile(self, site_key, site_url):
        if not self.api_key or not site_key or not site_url:
            raise ValueError('API key, site key and site URL must be provided and non-empty.')
        task_id = await self.submit_turnstile(site_key, site_url)
        token = await self.get_result(task_id)
        return token

async def interactive_solve():
    import sys
    api_key = input('Enter your CapSolver API key: ').strip()
    site_key = input('Enter the Turnstile site key: ').strip()
    site_url = input('Enter the site URL where CAPTCHA appears: ').strip()
    solver = CapSolver(api_key)
    try:
        token = await solver.solve_turnstile(site_key, site_url)
        print(f'CAPTCHA token: {token}')
    except Exception as e:
        print(f'Error during CAPTCHA solving: {e}')
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(interactive_solve())





