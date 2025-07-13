# -*- coding: utf-8 -*-
import asyncio
import websockets

async def handler(websocket, path):
    try:
        async for message in websocket:
            print(f"Received command: {message}")
            response = f"Executed: {message}"
            await websocket.send(response)
    except Exception as e:
        print(f"Error in handler: {e}")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())





