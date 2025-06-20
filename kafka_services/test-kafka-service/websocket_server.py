import asyncio
import websockets
from kafka import KafkaConsumer
import json

# Initialize Kafka consumer
consumer = KafkaConsumer(
    'rigcore-data',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Store connected WebSocket clients
clients = set()

async def register(websocket):
    clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        clients.remove(websocket)

async def broadcast(message):
    if clients:
        await asyncio.gather(
            *[client.send(json.dumps(message)) for client in clients]
        )

async def kafka_to_websocket():
    for message in consumer:
        await broadcast(message.value)

async def main():
    async with websockets.serve(register, "localhost", 8765):
        await kafka_to_websocket()

if __name__ == "__main__":
    asyncio.run(main())