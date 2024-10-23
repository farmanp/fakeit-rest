from fastapi import FastAPI
from api import app as api_app

app = FastAPI()

# Include the routes from api.py
app.include_router(api_app.router)