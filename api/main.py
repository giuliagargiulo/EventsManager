from fastapi import FastAPI
from .routers.base.base import router as base_router
from .routers.event.event import router as events_router
from .routers.participant.participant import router as participants_router

app = FastAPI()
app.include_router(base_router)
app.include_router(events_router)
app.include_router(participants_router)
