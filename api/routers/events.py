from fastapi import APIRouter, Depends
import os
from api import classes
from api import models
from api.database import get_db
from sqlalchemy.orm import Session
import os

router = APIRouter(prefix="/events", tags=["events"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FILES_DIR = os.path.join(BASE_DIR, "files")

# Save an event on a text file

@router.post("/save-to-file")
def save_event_to_file(event: classes.Event):
    file_path = os.path.join(FILES_DIR, "events.txt")
    with open(file_path, "a") as f:
        f.write(f"Event:{event.name} Date:{event.date} Location:{event.location} "
                f"Start Time:{event.start_time} End Time:{event.end_time}\n")
        return {"message": "Event saved to file successfully."}

# convert CSV to TXT

@router.post("/convert-file")
def convert_csv_to_txt():
    csv_file_path = os.path.join(FILES_DIR, "events.csv")
    txt_file_path = os.path.join(FILES_DIR, "events.txt")
    with open(csv_file_path, "r") as csv_f, open(txt_file_path, "a") as txt_f:
        for line in csv_f:
            txt_f.write(line.replace(",", " "))
    return {"message": "CSV file converted to TXT successfully."}

# CRUD Operations for Events
# CREATE

@router.post("/")
def create_event(event: classes.Event, db: Session = Depends(get_db)):
    db_event = models.Event(
        name=event.name,
        date=event.date,
        location=event.location,
        start_time=event.start_time,
        end_time=event.end_time)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

# READ

@router.get("/")
def get_events(db: Session = Depends(get_db)):
    return db.query(models.Event).all()


@router.get("/{event_id}")
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if event is None:
        return {"error": "Event not found"}
    return event

# UPDATE

@router.put("/{event_id}")
def update_event(event_id: int, event: classes.Event, db: Session = Depends(get_db)):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        return {"error": "Event not found"}
    db_event.name = event.name
    db_event.date = event.date
    db_event.location = event.location
    db_event.start_time = event.start_time
    db_event.end_time = event.end_time
    return db_event


# DELETE

@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        return {"error": "Event not found"}
    db.delete(db_event)
    db.commit()
    return {"message": "Event deleted successfully"}
