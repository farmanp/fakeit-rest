import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware to allow WebSocket connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/ws")
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
