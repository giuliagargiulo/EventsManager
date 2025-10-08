from fastapi import FastAPI
from .routers.base import router as base_router 
from .routers.events import router as events_router

app = FastAPI()
app.include_router(base_router)
app.include_router(events_router)
