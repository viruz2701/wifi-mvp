from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LocalUserBase(BaseModel):
    username: str
    venue_id: int
    user_profile_id: Optional[int] = None
    is_active: bool = True

class LocalUserCreate(LocalUserBase):
    password: str

class LocalUserUpdate(LocalUserBase):
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class LocalUserOut(LocalUserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True