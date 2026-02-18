from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VenueSocialActionBase(BaseModel):
    venue_id: int
    action_id: int
    reward_tariff_id: Optional[int] = None
    reward_duration_hours: int = 1

class VenueSocialActionCreate(VenueSocialActionBase):
    pass

class VenueSocialActionUpdate(BaseModel):
    reward_tariff_id: Optional[int] = None
    reward_duration_hours: Optional[int] = None

class VenueSocialActionOut(VenueSocialActionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True