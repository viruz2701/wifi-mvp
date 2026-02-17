from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SettingBase(BaseModel):
    key: str
    value: Optional[str] = None
    description: Optional[str] = None

class SettingCreate(SettingBase):
    pass

class SettingUpdate(BaseModel):
    value: Optional[str] = None
    description: Optional[str] = None

class SettingOut(SettingBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True