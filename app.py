from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.routing import APIRouter

from api import app as api_app  # Assuming that your existing REST API is in `api.py` file

app = FastAPI()

# Include your existing REST API routes
router = APIRouter()

router.include_router(api_app.router)
app.include_router(router)


# WebSocket endpoint that interacts directly with the client-generated data
@app.websocket("/ws/fake-events")
async def websocket_rest_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive data (as JSON string) from the client
            data = await websocket.receive_text()
            await websocket.send_text(f"Data received: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
