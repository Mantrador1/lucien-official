# -*- coding: utf-8 -*-
import asyncio
import websockets
import time

async def connect():
    uri = "ws://localhost:8765"
    retry_delay = 3
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to server.")
                while True:
                    command = input("Enter command (type 'exit' to quit): ")
                    if command.lower() == "exit":
                        print("Exiting client.")
                        return
                    await websocket.send(command)
                    response = await websocket.recv()
                    print(f"Response: {response}")
        except (websockets.ConnectionClosedError, ConnectionResetError) as e:
            print(f"Connection lost: {e}. Reconnecting in {retry_delay} seconds...")
            time.sleep(retry_delay)
        except Exception as e:
            print(f"Unexpected error: {e}. Reconnecting in {retry_delay} seconds...")
            time.sleep(retry_delay)

if __name__ == "__main__":
    asyncio.run(connect())





