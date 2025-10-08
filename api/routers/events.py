from fastapi import APIRouter
from .. import classes

router = APIRouter(prefix="/events", tags=["events"])

# Save an event on a text file
@router.post("/save-to-file")
def save_event_to_file(event: classes.Event):
    with open("../events.txt", "a") as f:
        f.write(f"Event:{event.name} Date:{event.date} Location:{event.location} "
                f"Start Time:{event.start_time} End Time:{event.end_time}\n")
        return {"message": "Event saved to file successfully."}

# convert CSV to TXT
@router.post("/convert-file")
def convert_csv_to_txt():
    with open("../events.csv", "r") as csv_f, open("../events.txt", "a") as txt_f:
        for line in csv_f:
            txt_f.write(line.replace(",", " ")) 
    return {"message": "CSV file converted to TXT successfully."}

# CRUD Operations for Events
# CREATE
@router.post("/")
def create_event(event: classes.Event):
    pass

# READ
@router.get("/")
def get_events():
    pass

@router.get("/{event_id}")
def get_event(event_id: int):
    pass

# UPDATE
@router.put("/{event_id}")
def update_event(event_id: int, event: classes.Event):
    pass

# DELETE
@router.delete("/{event_id}")
def delete_event(event_id: int):
    pass
