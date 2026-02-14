from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserProfileBase(BaseModel):
    mac_address: str
    phone_number: Optional[str] = None
    email: Optional[str] = None
    is_blocked: bool = False
    is_vip: bool = False
    device_oui: Optional[str] = None

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileUpdate(UserProfileBase):
    mac_address: Optional[str] = None

class UserProfileOut(UserProfileBase):
    id: int
    first_seen: datetime
    last_seen: Optional[datetime] = None
    total_sessions: int
    total_traffic_bytes: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True