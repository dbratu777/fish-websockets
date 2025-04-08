# data processing server socket

import asyncio
import base64
import os
import subprocess
import time
import websockets

async def listener(websocket):
    async for message in websocket:
        if message.startswith("IMAGE:"):
            image_data = message[len("IMAGE:"):]
            image_data = base64.b64decode(image_data)

            image_file_path = os.path.join('..', 'fish-websockets', 'received', f'{time.time()}.jpg')
            with open(image_file_path, "wb") as image_file:
                image_file.write(image_data)
            
            input_path = os.path.join('..', 'fish-websockets', 'received')
            output_path = os.path.join('..', 'fish-motion-detector', 'datasets', 'test')
            pred_util_path = os.path.join('..', 'fish-utils', 'predict-preprocessing', 'process-predict.py')
            subprocess.run(["python", pred_util_path, input_path, output_path])
            try:
                os.remove(image_file_path)
            except Exception as e:
                print(f"ERROR: could not delete {image_file_path} - {e}")
        else:
            print("ERROR: Unknown Message Type")

async def main():
    server = await websockets.serve(listener, "192.168.1.177", 1777)
    await server.wait_closed()

asyncio.run(main())
