from fastapi import WebSocket, WebSocketDisconnect


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
