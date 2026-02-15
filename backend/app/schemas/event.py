from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any

class EventBase(BaseModel):
    user_profile_id: Optional[int] = None
    venue_id: int
    type: str
    data: Optional[dict] = None

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    pass

class EventOut(EventBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True