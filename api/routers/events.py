from typing import List
from fastapi import APIRouter, Depends
import os
from api import classes
from api.database import get_db
from asyncpg import Connection


router = APIRouter(prefix="/events", tags=["events"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FILES_DIR = os.path.join(BASE_DIR, "files")

# Save an event on a text file

@router.post("/save-to-file",
             summary="Save Event to File",
             description="Save a new event in a text file",
             response_description="A message indicating the result of the save operation")
def save_event_to_file(event: classes.Event):
    file_path = os.path.join(FILES_DIR, "events.txt")
    with open(file_path, "a") as f:
        f.write(f"Event:{event.name} Date:{event.event_date} Location:{event.location} "
                f"Start Time:{event.start_time} End Time:{event.end_time}\n")
        return {"message": "Event saved to file successfully."}

# CRUD Operations for Events
# CREATE

@router.post("/",
             summary="Create an Event",
             description="Create a new event in the database",
             response_description="A message indicating the result of the creation operation")
async def create_event(event: classes.Event, db: Connection = Depends(get_db)):
    query = "INSERT INTO events (name, event_date, location, start_time, end_time) VALUES ($1, $2, $3, $4, $5) RETURNING id;"
    row = await db.fetchrow(query, event.name, event.event_date, event.location, event.start_time, event.end_time)
    return {"message": "Event created successfully", "id": row['id']}

# READ

@router.get("/",
             summary="Get All Events",
             description="Retrieve all events from the database",
             response_description="A list of events in JSON format",
             response_model=List[classes.Event])
async def get_events(db: Connection = Depends(get_db)):
    return await db.fetch("SELECT * FROM events;")


@router.get("/{event_id}",
             summary="Get Event by ID",
             description="Retrieve a specific event by its ID from the database",
             response_description="An event in JSON format",
             response_model=classes.Event)
async def get_event(event_id: int, db: Connection = Depends(get_db)):
    event = await db.fetchrow("SELECT * FROM events WHERE id = $1", event_id)
    if not event:
        return {"Error": "Event not found"}
    return event
    
# UPDATE

@router.put("/{event_id}",
             summary="Update an Event",
             description="Update an existing event in the database",
             response_description="A message indicating the result of the update operation")
async def update_event(event_id: int, event: classes.Event, db: Connection = Depends(get_db)):
    db_event = await db.fetchrow("SELECT * FROM events WHERE id = $1", event_id)
    if not db_event:
        return {"Error": "Event not found"}
    query = """
        UPDATE events SET name = $1, event_date = $2, location = $3,
        start_time = $4, end_time = $5 WHERE id = $6
    """
    values = (event.name, event.event_date, event.location, event.start_time, event.end_time, event_id)
    db.execute(query, *values)
    return {"message": "Event updated successfully"}

# DELETE

@router.delete("/{event_id}",
             summary="Delete an Event",
             description="Delete an event from the database",
             response_description="A message indicating the result of the deletion operation")
async def delete_event(event_id: int, db: Connection = Depends(get_db)):
    query = "DELETE FROM events WHERE id = $1"
    await db.execute(query, (event_id,))
    return {"message": "Event deleted successfully"}
