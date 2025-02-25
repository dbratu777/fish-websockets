# data processing server socket

import asyncio
import base64
import os
import time
import websockets

async def listener(websocket):
    async for message in websocket:
        if message.startswith("IMAGE:"):
            image_data = message[len("IMAGE:"):]
            image_data = base64.b64decode(image_data)

            image_file_name = os.path.join('..', 'fish-motion-detector', 'datasets', 'test', f'{time.time()}.jpg')
            with open(image_file_name, "wb") as image_file:
                image_file.write(image_data)
        else:
            print("ERROR: Unknown Message Type")

async def main():
    server = await websockets.serve(listener, "192.168.1.177", 1777)
    await server.wait_closed()

asyncio.run(main())
