from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class PortalTemplateBase(BaseModel):
    venue_id: int
    type: str  # 'auth', 'welcome', 'error'
    html_content: str
    css_files: List[str] = []
    js_files: List[str] = []
    images: List[str] = []
    is_active: bool = True

class PortalTemplateCreate(PortalTemplateBase):
    pass

class PortalTemplateUpdate(BaseModel):
    type: Optional[str] = None
    html_content: Optional[str] = None
    css_files: Optional[List[str]] = None
    js_files: Optional[List[str]] = None
    images: Optional[List[str]] = None
    is_active: Optional[bool] = None

class PortalTemplateOut(PortalTemplateBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True