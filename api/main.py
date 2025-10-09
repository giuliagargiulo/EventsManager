from fastapi import FastAPI
from .routers.base import router as base_router
from .routers.events import router as events_router
from .routers.participants import router as participants_router

app = FastAPI()
app.include_router(base_router)
app.include_router(events_router)
app.include_router(participants_router)
