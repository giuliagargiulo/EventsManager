from pydantic import BaseModel
from datetime import date, time

class Event(BaseModel):
    name: str
    date: date
    location: str
    start_time: time
    end_time: time

class Participant(BaseModel):
    name: str
    surname: str
    email: str
    phone: str
    