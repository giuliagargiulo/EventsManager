from fastapi import APIRouter
from .. import models

router = APIRouter(tags=["base"])

@router.get("/")
def root():
    return {"message": "Welcome to the Events Manager API!"}

@router.get("/greet")
def greet_user(name:str):
    return {"message" : f"Hello {name}, welcome to the Events Manager API!"}

@router.post("/events/save-to-file")
def save_event_to_file(event: models.Event):
    with open("../events.txt", "a") as f:
        f.write(f"ID:{event.id} Event:{event.name} Date:{event.date} Location:{event.location} "
                f"Start Time:{event.start_time} End Time:{event.end_time}\n")
        return {"message": "Event saved to file successfully."}

@router.post("/events/convert-file")
def convert_csv_to_txt():
    with open("../events.csv", "r") as csv_f, open("../events.txt", "a") as txt_f:
        for line in csv_f:
            txt_f.write(line.replace(",", " ")) 
    return {"message": "CSV file converted to TXT successfully."}

