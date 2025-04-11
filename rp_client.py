# raspberry pi client socket

import argparse
import asyncio
import base64
import os
import websockets


async def send_image(websocket, image_file_path):
    with open(image_file_path, "rb") as image_file:
        image_data = image_file.read()
        image_data = base64.b64encode(image_data).decode("utf-8")
        await websocket.send(f'IMAGE:{image_data}')
    print(f"[FISH-FRIEND::rp-client::LOG]: sent {image_file_path}.")


async def main():
    parser = argparse.ArgumentParser(
        description="Fish Friend's Web Server Client for Forwarding Fish Images to the Data Processing Server.")
    parser.add_argument("data", help="File Path to Image")
    args = parser.parse_args()

    server_addr = "ws://192.168.1.177:1777"
    try:
        async with websockets.connect(server_addr) as websocket:
            if os.path.exists(args.data):
                await send_image(websocket, args.data)
            else:
                print(
                    f"[FISH-FRIEND::rp-client::ERR]: file '{args.data}' does not exist.")
                return
    except websockets.exceptions.ConnectionClosedError:
        print(
            f'[FISH-FRIEND::rp-client::ERR]: connection to {server_addr} closed unexpectedly.')
    except websockets.exceptions.InvalidURI:
        print(f'[FISH-FRIEND::rp-client::ERR]: invalid URI: {server_addr}.')
    except (websockets.exceptions.WebSocketException, ConnectionRefusedError) as e:
        print(
            f'[FISH-FRIEND::rp-client::ERR]: could not Connect to the server at {server_addr}: {e}.')
    except Exception as e:
        print(
            f'[FISH-FRIEND::rp-client::ERR]: an unexpected error occurred: {e}.')

if __name__ == "__main__":
    asyncio.run(main())
