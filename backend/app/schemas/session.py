from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SessionBase(BaseModel):
    user_profile_id: Optional[int] = None
    venue_id: int
    nas_id: int
    mac_address: str
    ip_address: Optional[str] = None
    is_active: bool = True

class SessionCreate(SessionBase):
    pass

class SessionUpdate(SessionBase):
    session_end: Optional[datetime] = None
    traffic_in_bytes: Optional[int] = None
    traffic_out_bytes: Optional[int] = None
    is_active: Optional[bool] = None

class SessionOut(SessionBase):
    id: int
    session_start: datetime
    session_end: Optional[datetime] = None
    traffic_in_bytes: int
    traffic_out_bytes: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True