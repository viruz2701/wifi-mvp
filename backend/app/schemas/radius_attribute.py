from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RadiusAttributeBase(BaseModel):
    name: str
    vendor_id: Optional[int] = None
    is_proprietary: bool = False
    description: Optional[str] = None
    format_hint: Optional[str] = None

class RadiusAttributeCreate(RadiusAttributeBase):
    pass

class RadiusAttributeUpdate(BaseModel):
    name: Optional[str] = None
    vendor_id: Optional[int] = None
    is_proprietary: Optional[bool] = None
    description: Optional[str] = None
    format_hint: Optional[str] = None

class RadiusAttributeOut(RadiusAttributeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True