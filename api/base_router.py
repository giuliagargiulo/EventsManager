from fastapi import APIRouter

router = APIRouter(tags=["base"])

@router.get("/")
def root():
    return{"message": "Welcome to the Events Manager API!"}
