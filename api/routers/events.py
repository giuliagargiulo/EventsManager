from fastapi import APIRouter, Depends
import os
from api import classes
from api.database import get_db
from asyncpg import Connection


router = APIRouter(prefix="/events", tags=["events"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FILES_DIR = os.path.join(BASE_DIR, "files")

# Save an event on a text file

@router.post("/save-to-file")
def save_event_to_file(event: classes.Event):
    file_path = os.path.join(FILES_DIR, "events.txt")
    with open(file_path, "a") as f:
        f.write(f"Event:{event.name} Date:{event.event_date} Location:{event.location} "
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
async def create_event(event: classes.Event, db: Connection = Depends(get_db)):
    query = "INSERT INTO events (name, event_date, location, start_time, end_time) VALUES ($1, $2, $3, $4, $5) RETURNING id;"
    row = await db.fetchrow(query, event.name, event.event_date, event.location, event.start_time, event.end_time)
    return {"message": "Event created successfully", "id": row['id']}

# READ

@router.get("/")
async def get_events(db: Connection = Depends(get_db)):
    return await db.fetch("SELECT * FROM events;")


@router.get("/{event_id}")
async def get_event(event_id: int, db: Connection = Depends(get_db)):
    event = await db.fetchrow("SELECT * FROM events WHERE id = $1", event_id)
    if not event:
        return {"Error": "Event not found"}
    return event
    
# UPDATE

@router.put("/{event_id}")
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

@router.delete("/{event_id}")
async def delete_event(event_id: int, db: Connection = Depends(get_db)):
    query = "DELETE FROM events WHERE id = $1"
    await db.execute(query, (event_id,))
    return {"message": "Event deleted successfully"}
