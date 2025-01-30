# raspberry pi client socket

import asyncio
import base64
import websockets

async def send_message():
    server_addr = "ws://localhost:1777"
    try:
        async with websockets.connect(server_addr) as websocket:
            with open("image-for-processing.jpg", "rb") as image_file:
                image_data = image_file.read()
                image_data = base64.b64encode(image_data).decode("utf-8")
                await websocket.send(f'IMAGE:{image_data}')
    except websockets.exceptions.ConnectionClosedError:
        print(f'Connection to {server_addr} Closed Unexpectedly')
    except websockets.exceptions.InvalidURI:
        print(f'Invalid URI: {server_addr}')
    except (websockets.exceptions.WebSocketException, ConnectionRefusedError) as e:
        print(f'Could not Connect to the Server at {server_addr}: {e}')
    except Exception as e:
        print(f'An Unexpected Error Occurred: {e}')

asyncio.run(send_message())
