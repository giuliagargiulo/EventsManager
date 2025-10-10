from pydantic import BaseModel, Field, EmailStr
from datetime import date, time

class Event(BaseModel):
    name: str = Field(..., description="Name of the event", example="Tech Conference")
    event_date: date = Field(..., description="Date of the event", example="2026-05-01")
    location: str = Field(..., description="Location of the event", example="Lisbon")
    start_time: time = Field(..., description="Start time of the event", example="09:00:00")
    end_time: time = Field(..., description="End time of the event", example="17:00:00")

class Participant(BaseModel):
    name: str = Field(..., description="Name of the participant", example="Giulia")
    surname: str = Field(..., description="Surname of the participant", example="Gargiulo")
    email: EmailStr = Field(..., description="Email of the participant", example="giulia.gargiulo@example.com")
    phone: str = Field(..., description="Phone number of the participant", example="+123456789", max_length=15,)
