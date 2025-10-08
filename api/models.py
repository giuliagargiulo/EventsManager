from pydantic import BaseModel

class Event(BaseModel):
    name: str
    date: str
    location: str
    start_time: str
    end_time: str

class Participant(BaseModel):
    name: str
    surname: str
    email: str
    