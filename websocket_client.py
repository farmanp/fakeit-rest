import argparse
import asyncio
import json

import websockets


async def websocket_client(data_payload, num_records, delay):
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        for i in range(num_records):
            await websocket.send(json.dumps(data_payload))  # Send payload as JSON string
            response = await websocket.recv()  # Wait for response from the server
            print(f"Received: {response}")

            # Add delay between sending messages if specified
            if delay > 0:
                await asyncio.sleep(delay)


# Main function to parse arguments and run the client
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WebSocket Client to send data to WebSocket server.")
    parser.add_argument("--data", type=str, required=True, help="JSON string to be sent to the WebSocket server.")
    parser.add_argument("--num_records", type=int, default=1, help="Number of times to send the payload.")
    parser.add_argument("--delay", type=float, default=0, help="Delay in seconds between each message.")

    args = parser.parse_args()

    # Parse the input JSON string
    try:
        payload = json.loads(args.data)
    except json.JSONDecodeError:
        print("Invalid JSON format provided. Please provide a valid JSON string.")
        exit(1)

    # Run the client with the constructed payload, number of records, and delay
    asyncio.run(websocket_client(payload, args.num_records, args.delay))
