from fastapi import APIRouter
from api import classes

router = APIRouter(tags=["base"])

@router.get("/")
def root():
    return {"message": "Welcome to the Events Manager API!"}

@router.get("/greet")
def greet_user(name:str):
    return {"message" : f"Hello {name}, welcome to the Events Manager API!"}
