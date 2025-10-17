from typing import List
from fastapi import APIRouter, Depends
import os
import uuid
from databases import Database
from api.database import get_db
from pydantic import BaseModel, Field
from datetime import date, time

BASE_DIR = os.getenv("BASE_DIR", "/app")
FILES_DIR = os.getenv("FILES_DIR", "/app/files")

router = APIRouter(prefix="/events", tags=["events"])


class Event(BaseModel):
    name: str = Field(...,
                      description="Name of the event",
                      example="Tech Conference")
    event_date: date = Field(...,
                             description="Date of the event",
                             example="2026-05-01")
    location: str | None = Field(...,
                                 description="Location of the event",
                                 example="Lisbon")
    start_time: time = Field(...,
                             description="Start time of the event",
                             example="09:00:00")
    end_time: time = Field(...,
                           description="End time of the event",
                           example="17:00:00")


class EventOut(Event):
    uu_id: uuid.UUID = Field(...,
                             description="UUID version 7 of the event",
                             example="123e4567-e89b-12d3-a456-426614174000")


class EventBrief(BaseModel):
    uu_id: uuid.UUID = Field(...,
                             description="UUID version 7 of the event",
                             example="123e4567-e89b-12d3-a456-426614174000")
    name: str = Field(...,
                      description="Name of the event",
                      example="Tech Conference")

# Save an event on a text file


@router.post("/save-to-file",
             summary="Save Event to File",
             description="Save a new event in a text file",
             response_description="A message indicating the result of the save operation")
def save_event_to_file(event: Event):
    file_path = os.path.join(FILES_DIR, "events.txt")
    with open(file_path, "a") as f:
        f.write(f"Event:{event.name} Date:{event.event_date} Location:{event.location} "
                f"Start Time:{event.start_time} End Time:{event.end_time}\n")
        return {"message": "Event saved to file successfully."}

# CRUD Operations
# CREATE


@router.post("/",
             summary="Create an Event",
             description="Create a new event in the database",
             response_description="A message indicating the result of the creation operation")
async def create_event(event: Event, db: Database = Depends(get_db)):
    query = ("INSERT INTO tbl_event (name, event_date, location, start_time, end_time) "
             "VALUES (:name, :event_date, :location, :start_time, :end_time) "
             "RETURNING uu_id;")
    q_data = event.dict()
    row = await db.fetch_one(query=query, values=q_data)
    return {"message": "Event created successfully", "id": row['uu_id']}

# READ


@router.get("/",
            summary="Get All Events",
            description="Retrieve all events from the database",
            response_description="A list of events in JSON format",
            response_model=List[EventBrief])
async def get_events(db: Database = Depends(get_db)):
    query = ("SELECT uu_id, name "
             "FROM tbl_event;")
    records = await db.fetch_all(query)
    return [dict(record) for record in records]


@router.get("/{event_id}",
            summary="Get Event by ID",
            description="Retrieve a specific event by its ID from the database",
            response_description="An event in JSON format",
            response_model=EventOut)
async def get_event(event_id: str, db: Database = Depends(get_db)):
    query = ("SELECT name, event_date, location, start_time, end_time, uu_id "
             "FROM tbl_event te "
             "WHERE uu_id = :uu_id;")
    q_data = {"uu_id": event_id}
    db_event = await db.fetch_one(query=query, values=q_data)
    if not db_event:
        return {"Error": "Event not found"}
    return dict(db_event)

# UPDATE


@router.put("/{event_id}",
            summary="Update an Event",
            description="Update an existing event in the database",
            response_description="A message indicating the result of the update operation")
async def update_event(event_id: str, event: Event, db: Database = Depends(get_db)):
    q_data = {"uu_id": event_id}
    query = ("SELECT uu_id, name "
             "FROM tbl_event "
             "WHERE uu_id = :uu_id;")
    db_event = await db.fetch_one(query=query, values=q_data)
    if not db_event:
        return {"Error": "Event not found"}
    query = ("UPDATE tbl_event "
             "SET name = :name, "
             "    event_date = :event_date, "
             "    location = :location, "
             "    start_time = :start_time, "
             "    end_time = :end_time "
             "WHERE uu_id = :uu_id;")
    q_data = {"name": event.name,
              "event_date": event.event_date,
              "location": event.location,
              "start_time": event.start_time,
              "end_time": event.end_time,
              "uu_id": event_id}
    await db.execute(query=query, values=q_data)
    return {"message": "Event updated successfully"}

# DELETE


@router.delete("/{event_id}",
               summary="Delete an Event",
               description="Delete an event from the database",
               response_description="A message indicating the result of the deletion operation")
async def delete_event(event_id: str, db: Database = Depends(get_db)):
    query = ("SELECT uu_id "
             "FROM tbl_event "
             "WHERE uu_id = :uu_id;")
    q_data = {"uu_id": event_id}
    db_event = await db.fetch_one(query=query, values=q_data)
    if not db_event:
        return {"Error": "Event not found"}
    query = ("DELETE FROM tbl_event "
             "WHERE uu_id = :uu_id;")
    await db.execute(query=query, values=q_data)
    return {"message": "Event deleted successfully"}
