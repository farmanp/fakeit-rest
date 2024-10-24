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
            if data == "generate-single":
                response = {"message": "Generated single data successfully"}
                await websocket.send_json(response)
            else:
                await websocket.send_text(f"Unknown command: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
