import asyncio
import json

import websockets
from faker import Faker

fake = Faker()


# Function to generate fake data
def generate_single_data():
    return {"name": fake.first_name(), "email": fake.email()}


async def websocket_client():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        for _ in range(20):  # Loop to run for approximately 20 iterations
            data = generate_single_data()
            await websocket.send(json.dumps(data))  # Send data as JSON string
            response = await websocket.recv()  # Wait for the server response
            print(f"Received: {response}")
            await asyncio.sleep(1)  # Wait for 1 second before the next request


# Run the client
if __name__ == "__main__":
    asyncio.run(websocket_client())
