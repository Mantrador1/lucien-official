import os
import asyncio
import httpx

async def start_farming():
    fly_url = os.getenv('FLY_APP_URL')
    api_key = os.getenv('OPENROUTER_API_KEY')
    claude_model = os.getenv('CLAUDE_MODEL')

    if not fly_url or not api_key or not claude_model:
        print('❌ Missing environment variables. Please set FLY_APP_URL, OPENROUTER_API_KEY, and CLAUDE_MODEL.')
        return

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    json_data = {'model': claude_model}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(fly_url.rstrip('/') + '/start', headers=headers, json=json_data)
            response.raise_for_status()
            print('✅ Farming started successfully.')
            print('Response:', response.json())
        except httpx.HTTPStatusError as exc:
            print(f'❌ HTTP error: {exc.response.status_code} - {exc.response.text}')
        except Exception as e:
            print(f'❌ Unexpected error: {e}')

if __name__ == '__main__':
    asyncio.run(start_farming())




