from fastapi import APIRouter, WebSocket

from websocket_handler import handle_websocket

websocket_router = APIRouter()


@websocket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await handle_websocket(websocket)
