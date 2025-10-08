from fastapi import FastAPI
from . import models

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the Events Manager API!"}

@app.get("/greet")
def greet_user(name:str):
    return {"message" : f"Hello {name}, welcome to the Events Manager API!"}

@app.post("/events/save-to-file")
def save_event_to_file(event: models.CreateEvent):
    with open("../events.txt", "w") as f:
        f.write(f"Event:{event.name} Date:{event.date} Location:{event.location} "
                f"Start Time:{event.start_time} End Time:{event.end_time}\n")
        return {"message": "Event saved to file successfully."}
    