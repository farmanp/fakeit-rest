import json

from fastapi import WebSocket, WebSocketDisconnect


async def handle_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            try:
                # Parse the incoming data as JSON
                payload = json.loads(data)

                if isinstance(payload, dict) and "name" in payload and "email" in payload:
                    # Example of a customized response with the received data
                    response = {
                        "name": payload["name"],
                        "email": payload["email"],
                    }
                    await websocket.send_json(response)
                else:
                    response = {"error": "Invalid payload structure"}
                    await websocket.send_json(response)

            except json.JSONDecodeError:
                await websocket.send_text(f"Unknown command or invalid JSON: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
