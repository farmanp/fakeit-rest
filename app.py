from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import rest_router
from websocket_router import websocket_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(rest_router)
app.include_router(websocket_router)
