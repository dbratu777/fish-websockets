# data processing client socket

import argparse
import asyncio
import base64
import os
import websockets

"""
# this should be included in whatever script is passing data to dp_client.py (alert_json is passed to it as alert data)
import datetime
import json
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# ALERT INFO: 
# Types: 0 = Temp, 1 = pH, 2 = ORP, 3 = Fish Health
class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True)
    type = Column(Integer, nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(200), nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    read = Column(Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'description': self.description,
            'timestamp': self.timestamp.isoformat(),
            'read': self.read
        }
    
# example usage: 
alert = Alert(type=3, title="Fish Health", description="Example Desc.")
alert_dict = alert.to_dict()
alert_json = json.dumps(alert_dict)
"""

async def send_alert(websocket, message):
    await websocket.send(f'TEXT:{message}')

async def send_heatmap(websocket, image_file_path):
    with open(image_file_path, "rb") as image_file:
        image_data = image_file.read()
        image_data = base64.b64encode(image_data).decode("utf-8")
        await websocket.send(f'IMAGE:{image_data}')

async def main():
    parser = argparse.ArgumentParser(description="Fish Friend's Data Processing Client for Forwarding Heatmap Images or Location-Based Alerts to the Web Server.")
    parser.add_argument("type", choices=["alert", "heatmap"], help="Type of Message to Send.")
    parser.add_argument("data", help="Alert Text or File Path to Heatmap")
    args = parser.parse_args()

    server_addr = "ws://localhost:2777"
    try: 
        async with websockets.connect(server_addr) as websocket:
            if args.type == "alert":
                await send_alert(websocket, args.data)
            elif args.type == "heatmap":
                if os.path.exists(args.data):
                    await send_heatmap(websocket, args.data)
                else:
                    print(f"Error: The file '{args.data}' does not exist.")
                    return
    except websockets.exceptions.ConnectionClosedError:
        print(f'Connection to {server_addr} Closed Unexpectedly')
    except websockets.exceptions.InvalidURI:
        print(f'Invalid URI: {server_addr}')
    except (websockets.exceptions.WebSocketException, ConnectionRefusedError) as e:
        print(f'Could not Connect to the Server at {server_addr}: {e}')
    except Exception as e:
        print(f'An Unexpected Error Occurred: {e}')

if __name__ == "__main__":
    asyncio.run(main())
