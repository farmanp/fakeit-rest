from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import rest_router  # Import the router defined in api.py
from websocket_endpoint import websocket_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the REST API router from api.py
app.include_router(rest_router)

# Include the WebSocket router from websocket_endpoint.py
app.include_router(websocket_router)
