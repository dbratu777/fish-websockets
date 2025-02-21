# raspberry pi server socket

import asyncio
import base64
import datetime
import json
import time
import websockets

from contextlib import contextmanager
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

# Set up the database engine
engine = create_engine('sqlite:///../fish-flask-app/instance/values.db', echo=True) 
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
    finally:
        session.close()

def create_alert(session, alert_data):
    alert_json = json.loads(alert_data)
    alert_entry = Alert(
        type=alert_json['type'], 
        title=alert_json['title'], 
        description=alert_json['description'], 
        timestamp=alert_json['timestamp']
    )
    session.add(alert_entry)

async def listener(websocket):
    async for message in websocket:
        if message.startswith("IMAGE:"):
            image_data = message[len("IMAGE:"):]
            image_data = base64.b64decode(image_data)

            image_file_name = f'../fish-flask-app/static/images/heatmap-{time.time()}.jpg'
            with open(image_file_name, "wb") as image_file:
                image_file.write(image_data)
        elif message.startswith("TEXT:"):
            alert_data = message[len("TEXT:"):]
            with session_scope() as session:
                create_alert(session, alert_data)
                session.commit()
        else:
            print("ERROR: Unknown Message Type")

async def main():
    server = await websockets.serve(listener, "localhost", 2777)
    await server.wait_closed()

asyncio.run(main())
