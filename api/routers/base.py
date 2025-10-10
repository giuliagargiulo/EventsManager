from fastapi import APIRouter
from api import classes

router = APIRouter(tags=["base"])

@router.get("/",
            summary="Root Endpoint",
            description="Return a welcome message",
            response_description="A welcome message in JSON format")
def root():
    return {"message": "Welcome to the Events Manager API!"}

@router.get("/greet",
            summary="Greet Endpoint",
            description="Return a welcome message for the user",
            response_description="A personalised welcome message in JSON format")
def greet_user(name:str):
    return {"message" : f"Hello {name}, welcome to the Events Manager API!"}
