from pydantic import BaseModel

class EventBase(BaseModel):
    name: str
    date: str
    location: str
    start_time: str
    end_time: str

class Event(EventBase):
    id: int

class CreateEvent(EventBase):
    pass

    