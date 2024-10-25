import json

from fastapi import WebSocket, WebSocketDisconnect

from faker_data_generation_service import generate_fake_data


# Use the same function as in the REST API to generate data
async def handle_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            try:
                # Parse the incoming data as JSON
                payload = json.loads(data)

                if isinstance(payload, dict) and "fields" in payload:
                    # Use the Faker generation function to create fake data
                    fields = payload["fields"]

                    # Assuming the payload follows the schema to generate Faker data
                    generated_data = generate_fake_data({"fields": fields}, 1)

                    response = {"data": generated_data[0], "message": "Data generated successfully"}
                    await websocket.send_json(response)
                else:
                    response = {"error": "Invalid payload structure. Expected 'fields' key."}
                    await websocket.send_json(response)

            except json.JSONDecodeError:
                await websocket.send_text(f"Unknown command or invalid JSON: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
