from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SMSCodeBase(BaseModel):
    phone_number: str
    code: str
    expires_at: datetime

class SMSCodeCreate(SMSCodeBase):
    pass

class SMSCodeUpdate(BaseModel):
    is_used: Optional[bool] = None
    attempts: Optional[int] = None

class SMSCodeOut(SMSCodeBase):
    id: int
    is_used: bool
    attempts: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True