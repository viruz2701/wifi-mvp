from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BannerBase(BaseModel):
    venue_id: int
    image_url: Optional[str] = None
    target_url: str
    is_active: bool = True

class BannerCreate(BannerBase):
    pass

class BannerUpdate(BaseModel):
    image_url: Optional[str] = None
    target_url: Optional[str] = None
    is_active: Optional[bool] = None

class BannerOut(BannerBase):
    id: int
    clicks_count: int
    impressions_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True