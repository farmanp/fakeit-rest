import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

websocket_router = APIRouter()


@websocket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            try:
                # Try parsing data as JSON
                payload = json.loads(data)
                if isinstance(payload, dict) and "name" in payload and "email" in payload:
                    # Customize the response with additional data or information
                    response = {
                        "name": payload["name"],
                        "email": payload["email"],
                    }
                    await websocket.send_json(response)
                else:
                    response = {"error": "Invalid payload structure"}
                    await websocket.send_json(response)
            except json.JSONDecodeError:
                # If not JSON, consider it as an unknown command
                await websocket.send_text(f"Unknown command: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
