import argparse
import asyncio
import json

import websockets


async def websocket_client(payload):
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(payload))  # Send payload as JSON string
        response = await websocket.recv()  # Wait for response from the server
        print(f"Received: {response}")


# Main function to parse arguments and run the client
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WebSocket Client to send data to WebSocket server.")
    parser.add_argument("--data", type=str, required=True, help="JSON string to be sent to the WebSocket server.")

    args = parser.parse_args()

    # Parse the input JSON string
    try:
        payload = json.loads(args.data)
    except json.JSONDecodeError:
        print("Invalid JSON format provided. Please provide a valid JSON string.")
        exit(1)

    # Run the client with the constructed payload
    asyncio.run(websocket_client(payload))
