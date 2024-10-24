import asyncio

import websockets
from faker import Faker

fake = Faker()


# Function to generate fake data
def generate_single_data():
    return {"name": fake.first_name(), "email": fake.email()}


async def websocket_client():
    uri = "ws://localhost:8000/ws/fake-events"  # Make sure the URI matches the server's WebSocket endpoint
    async with websockets.connect(uri) as websocket:
        for _ in range(20):  # Loop to run for approximately 1 minute (20 iterations of 3 seconds each)
            data = generate_single_data()  # Generate data locally
            await websocket.send(str(data))  # Send the generated data as a string to the WebSocket server
            response = await websocket.recv()  # Wait for the response from the server
            print(f"Received: {response}")
            await asyncio.sleep(3)  # Wait for 3 seconds before the next request


# Run the client
if __name__ == "__main__":
    asyncio.run(websocket_client())
